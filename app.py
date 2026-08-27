from pathlib import Path

import gradio as gr

from asr_client import transcribe_audio
from dify_client import ask_dify
from tts_client import synthesize_speech


def run_voice_agent(audio_path):
    """完成一次语音问答：ASR → Dify / DeepSeek → TTS。"""

    if not audio_path:
        raise gr.Error("请先录音或上传一个音频文件。")

    try:
        question = transcribe_audio(audio_path).strip()

        if not question:
            raise RuntimeError("没有识别出有效文字，请重新录音。")

        answer = ask_dify(question).strip()

        if not answer:
            raise RuntimeError("Dify 没有返回有效回答。")

        answer_audio_path = synthesize_speech(answer)

        return (
            question,
            answer,
            str(answer_audio_path),
            "✅ 处理完成",
        )

    except Exception as error:
        raise gr.Error(str(error)) from error


CUSTOM_CSS = """
:root {
    --page-bg: #f4f5f8;
    --surface: #ffffff;
    --surface-soft: #f8f8fb;
    --primary: #655cf3;
    --primary-hover: #554ce3;
    --primary-soft: #eeecff;
    --text-main: #202231;
    --text-muted: #777b8d;
    --border: #e5e6ed;
    --shadow: 0 22px 70px rgba(42, 44, 74, 0.10);
}


/* 页面 */

html,
body {
    min-width: 1000px;
    background: var(--page-bg) !important;
}

body,
.gradio-container {
    background:
        radial-gradient(
            circle at 50% -12%,
            rgba(101, 92, 243, 0.15),
            transparent 34%
        ),
        linear-gradient(
            180deg,
            #fafaff 0%,
            var(--page-bg) 75%
        ) !important;
}

.gradio-container {
    width: calc(100vw - 64px) !important;
    min-width: 960px !important;
    max-width: 1240px !important;
    margin: 0 auto !important;
    padding: 34px 0 50px !important;
}


/* 顶部标题 */

#hero {
    margin-bottom: 24px;
    padding: 30px 36px;
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 30px;
    background:
        linear-gradient(
            135deg,
            rgba(101, 92, 243, 0.09),
            rgba(255, 255, 255, 0.96)
        );
    box-shadow: var(--shadow);
}

.hero-top {
    display: flex;
    align-items: center;
    gap: 16px;
}

.hero-icon {
    width: 54px;
    height: 54px;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    border-radius: 18px;
    color: white;
    font-size: 26px;
    background: linear-gradient(135deg, #8179ff, #554ce3);
    box-shadow: 0 12px 28px rgba(101, 92, 243, 0.30);
}

.hero-copy h1 {
    margin: 0;
    color: var(--text-main);
    font-size: 30px;
    font-weight: 760;
    letter-spacing: -0.6px;
}

.hero-copy p {
    margin: 6px 0 0;
    color: var(--text-muted);
    font-size: 14px;
}

.flow {
    margin-top: 21px;
    display: flex;
    align-items: center;
    gap: 9px;
    color: #696d7e;
    font-size: 13px;
}

.flow-step {
    padding: 7px 11px;
    border: 1px solid #e1e0fb;
    border-radius: 999px;
    background: rgba(238, 236, 255, 0.72);
    color: #5c54d4;
    font-weight: 650;
}

.flow-arrow {
    color: #a2a5b2;
}


/* 主体卡片 */

.app-card {
    height: 100%;
    padding: 24px;
    border: 1px solid var(--border);
    border-radius: 26px !important;
    background: var(--surface);
    box-shadow:
        0 14px 45px rgba(42, 44, 74, 0.07),
        0 2px 10px rgba(42, 44, 74, 0.04);
}

.card-title {
    margin: 0 0 15px;
    color: var(--text-main);
    font-size: 16px;
    font-weight: 720;
}

.card-subtitle {
    margin: -8px 0 18px;
    color: var(--text-muted);
    font-size: 12px;
}


/* 统一圆角 */

.app-card,
.app-card > div,
.gr-group,
.gr-box,
.gr-form,
textarea,
input,
select,
button,
.gr-button,
.audio-container,
.wrap,
.toast,
.toast-wrap > div,
.error,
.warning {
    border-radius: 16px !important;
}


/* 音频输入 */

#audio-input {
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: var(--surface-soft) !important;
}

#audio-input > div,
#audio-input .wrap,
#audio-input .audio-container {
    border-radius: 18px !important;
}


/* 按钮 */

#submit-button {
    min-height: 48px !important;
    margin-top: 16px;
    border: none !important;
    border-radius: 16px !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    background: linear-gradient(
        135deg,
        #7068f7,
        var(--primary)
    ) !important;
    box-shadow: 0 11px 25px rgba(101, 92, 243, 0.26);
}

#submit-button:hover {
    background: linear-gradient(
        135deg,
        #655df0,
        var(--primary-hover)
    ) !important;
    box-shadow: 0 13px 29px rgba(101, 92, 243, 0.32);
}

#clear-button {
    min-height: 42px !important;
    color: #666a7b !important;
    background: #f7f7fa !important;
    border: 1px solid #dedfe7 !important;
}

#clear-button:hover {
    color: var(--primary) !important;
    border-color: #bbb7fa !important;
    background: #f3f1ff !important;
}


/* 文本输出 */

#question-output textarea,
#answer-output textarea,
#status-output textarea {
    border: 1px solid var(--border) !important;
    border-radius: 17px !important;
    color: var(--text-main) !important;
    background: var(--surface-soft) !important;
    box-shadow: none !important;
}

#question-output textarea {
    min-height: 126px !important;
}

#answer-output textarea {
    min-height: 254px !important;
    line-height: 1.7 !important;
}

#status-output textarea {
    min-height: 46px !important;
    color: #4e5767 !important;
    font-weight: 650 !important;
}


/* 底部音频回答 */

#audio-card {
    margin-top: 24px;
}

#audio-output {
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: var(--surface-soft) !important;
}

#audio-output > div,
#audio-output .wrap,
#audio-output .audio-container {
    border-radius: 18px !important;
}


/* 缩小 Gradio 默认标签的视觉重量 */

label,
.block-info,
.svelte-1gfkn6j {
    color: #666a7b !important;
    font-weight: 650 !important;
}


/* 隐藏底部多余信息 */

footer {
    display: none !important;
}
"""


with gr.Blocks(
    title="Tyra Voice Agent",
    theme=gr.themes.Soft(
        primary_hue="indigo",
        neutral_hue="slate",
    ),
    css=CUSTOM_CSS,
) as demo:

    gr.HTML(
        """
        <section id="hero">
            <div class="hero-top">
                <div class="hero-icon">⌁</div>

                <div class="hero-copy">
                    <h1>Tyra Voice Agent</h1>
                    <p>
                        基于 SenseVoiceSmall、Dify / DeepSeek 与
                        MOSS-TTS-Nano 的语音问答系统
                    </p>
                </div>
            </div>

            <div class="flow">
                <span class="flow-step">语音输入</span>
                <span class="flow-arrow">→</span>
                <span class="flow-step">ASR 识别</span>
                <span class="flow-arrow">→</span>
                <span class="flow-step">LLM 回答</span>
                <span class="flow-arrow">→</span>
                <span class="flow-step">TTS 合成</span>
            </div>
        </section>
        """
    )

    with gr.Row(equal_height=True):
        with gr.Column(scale=5, elem_classes="app-card"):
            gr.HTML(
                """
                <div class="card-title">录音或上传问题</div>
                <div class="card-subtitle">
                    录制一段语音，或上传本地音频文件
                </div>
                """
            )

            input_audio = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                format="wav",
                label="语音输入",
                show_label=False,
                elem_id="audio-input",
            )

            submit_button = gr.Button(
                "开始语音问答",
                variant="primary",
                size="lg",
                elem_id="submit-button",
            )

            clear_button = gr.ClearButton(
                value="清空内容",
                components=[],
                elem_id="clear-button",
            )

            status_output = gr.Textbox(
                label="运行状态",
                value="等待输入",
                interactive=False,
                lines=1,
                elem_id="status-output",
            )

        with gr.Column(scale=7, elem_classes="app-card"):
            gr.HTML(
                """
                <div class="card-title">识别与回答</div>
                <div class="card-subtitle">
                    页面会显示语音识别结果和 DeepSeek 的回答
                </div>
                """
            )

            question_output = gr.Textbox(
                label="ASR 识别结果",
                lines=4,
                placeholder="这里会显示识别出的文字",
                interactive=False,
                elem_id="question-output",
            )

            answer_output = gr.Textbox(
                label="DeepSeek 回答",
                lines=9,
                placeholder="这里会显示大模型生成的回答",
                interactive=False,
                elem_id="answer-output",
            )

    with gr.Group(elem_classes="app-card", elem_id="audio-card"):
        gr.HTML(
            """
            <div class="card-title">语音回答</div>
            <div class="card-subtitle">
                MOSS-TTS-Nano 生成的回答音频
            </div>
            """
        )

        audio_output = gr.Audio(
            label="TTS 语音回答",
            show_label=False,
            autoplay=True,
            elem_id="audio-output",
        )

    submit_button.click(
        fn=run_voice_agent,
        inputs=input_audio,
        outputs=[
            question_output,
            answer_output,
            audio_output,
            status_output,
        ],
    )

    clear_button.add(
        [
            input_audio,
            question_output,
            answer_output,
            audio_output,
            status_output,
        ]
    )


if __name__ == "__main__":
    moss_output_dir = (
        Path.home()
        / "Projects"
        / "MOSS-TTS-Nano"
        / "generated_audio"
    )

    demo.launch(
        inbrowser=True,
        allowed_paths=[str(moss_output_dir)],
    )
