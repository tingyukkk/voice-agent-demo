# Voice Agent Demo

一个简单的端到端语音问答 Agent Demo。

用户可以通过录音或上传音频提出问题，系统会依次完成：

```text
语音输入
→ ASR 语音识别
→ LLM 生成回答
→ TTS 语音合成
→ 返回文字和语音结果
```

## 技术栈

* **ASR:** SenseVoiceSmall / FunASR
* **LLM:** DeepSeek via Dify
* **TTS:** MOSS-TTS-Nano
* **Web UI:** Gradio
* **Language:** Python

## 功能

* 浏览器录音
* 上传本地音频
* 自动语音识别
* 调用 LLM 生成回答
* 自动生成语音回答
* 在网页端展示识别文本、回答文本和音频

## 运行

首先进入项目环境：

```bash
conda activate voice-agent
```

然后运行：

```bash
python app.py
```

浏览器打开：

```text
http://127.0.0.1:7860
```

## 配置

项目使用 `.env` 保存 Dify API 配置。


## 项目结构

```text
app.py            # Gradio 主界面
asr_client.py     # ASR
dify_client.py    # LLM / Dify
tts_client.py     # TTS
voice_chat.py     # 命令行版本
```


## 当前状态

该项目目前作为一个 **Proof of Concept**，主要用于实践 ASR、LLM 和 TTS 的端到端系统集成。

目前完整流程已经跑通：

```text
Speech → ASR → LLM → TTS → Speech
```
