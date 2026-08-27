from pathlib import Path
from time import perf_counter

from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess


print("正在加载 SenseVoiceSmall 模型……")

load_start = perf_counter()

# 模型在程序启动时加载一次，后面可以反复识别音频
asr_model = AutoModel(
    model="iic/SenseVoiceSmall",
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cpu",
)

print(f"模型加载完成，耗时：{perf_counter() - load_start:.2f} 秒")


def transcribe_audio(audio_path: str) -> str:
    """识别一个本地音频文件，返回文字。"""

    path = Path(audio_path)

    if not path.exists():
        raise FileNotFoundError(f"找不到音频文件：{path}")

    start = perf_counter()

    result = asr_model.generate(
        input=str(path),
        cache={},
        language="auto",
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )

    if not result or "text" not in result[0]:
        raise RuntimeError(f"ASR 没有返回有效结果：{result}")

    text = rich_transcription_postprocess(result[0]["text"])

    print(f"ASR 识别耗时：{perf_counter() - start:.2f} 秒")

    return text


def main():
    """直接运行本文件时，用于测试 ASR。"""

    audio_path = input("请输入音频文件名或路径：").strip()

    if not audio_path:
        print("音频路径不能为空。")
        return

    try:
        text = transcribe_audio(audio_path)

        print("\n识别结果：")
        print(text)

    except (FileNotFoundError, RuntimeError) as error:
        print("\n识别失败：")
        print(error)


if __name__ == "__main__":
    main()