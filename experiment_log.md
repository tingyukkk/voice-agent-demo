# Voice Agent Demo 实验日志
## 目标
用 DeepSeek 的 API，以 dify 作为工具进行封装，接入 ASR 和 TTS（小，开源），组成一个建议语音问答系统。

## 开发环境
- 设备：Apple Silicon MacBook Air
- 电脑架构：arm64
- python：3.10.20
- 编辑器：VS code
- conda环境：voice agent

## 进度

### 2026-7-24

#### 1. DeepSeek 与 dify 的网页端配置
- DeepSeek API 获取和 dify 注册
- dify 中配置 DS
- 创建 Tyra Voice Agent
- 网页测试成功

#### 2. dify API 终端测试
- 获取 dify API key
- API 能被调用
- python 代码能被调用

#### 3. 配置本地 python 环境
- 安装 miniforge
- 初始化 Conda
- 搭建 voice-agent 环境
- 使用 VS code 运行 python 并选择 voice agent 作为解释器

#### 4. 在 VS code 中调用 dify
- 创建 .env 保护密钥
- 编写 dify_client.py 
- 终端测试调用成功

### 遇到的问题

#### 问题一
现象：安装 miniforge 后运行 conda 提示 command not found
解决：找到 miniforge 的路径，执行 conda init zsh，再次运行成功

#### 问题二
现象：dify 调用时报错400
报错信息：400 Client Error: Bad Request for url: https://api.dify.ai/v1/chat-messages
(voice-agent) tingyukleung@Tyras-MacBook-Air voice-agent-demo % 
排查：修改错误处理，使其打印服务器返回详情
原因：原先使用的模型 deepseek-chat 从7.24起停止支持
解决：dify 中修改使用模型为 deepseek-v4-flash，再次运行成功

### 2026-7-26

#### 1. 配置 funASR 到 voice agent 环境
- 选择 SenseVoiceSmall 模型，国内团队，开源，小型 ASR
- 安装 pytorch、funASR
- 使用官方测试音频进行识别
模型加载耗时：305。29 秒
识别结果：甚至至出现交易几乎停滞的情况。
识别耗时：1.04 秒

- 使用本地音频进行测试
实际说的话： Give me a plain explanation of shell.
识别结果：Give me a plain explanation of shell.
模型加载耗时：3.87 秒
识别耗时：0.69 秒

实际说的话：请解释一下 shell 的意思。
识别结果：🎼请解释一下sll的意思。
模型加载耗时：3.42 秒
识别耗时：0.62 秒

模型能够正确识别大部分中文，但把中间的英文技术词 shell 识别成了 sll，同时将录音中的部分声音判断为音乐事件。
说明模型已经能够处理本地录音，但中英文混合和专业词汇的识别准确率仍需进一步测试。

实际说的话：请解释一下 Linux Shell 的意思。
识别结果：🎼请解释一下linux show的意思。
模型加载耗时：4.68 秒
识别耗时：0.65 秒

加入 Linux 作为上下文后，Linux 可以被正确识别，但 shell 仍被识别为 show。
说明模型能够完成中文语音识别，但对中英文混合的技术词识别不够稳定。

对于一开始的英文测试，纯英文语句 “Give me a plain explanation of shell.”
可以被完整正确识别。由此判断，模型能够识别 shell 这个英文单词，但在中文句子中夹杂英文技术词时容易出现误识别，问题主要集中在中英混合场景。

为排除音频格式的影响，我将同一段 M4A 录音用 ffmpeg 转换为 16 kHz 单声道 WAV 后重新测试，识别结果没有明显变化。因此本次误识别更可能来自模型对中英混合技术词的处理能力，而不是音频格式。

#### 2. 把 funASR 和 dify 接起来
- 整理 dify_client.py, 将其变为可复用的一个模块，既可以直接执行 main() 手动测试，也可以被其他文件 import
- 编写 voice_chat.py，存放 question 和 dify 的回答
- 将语音识别结果发送给 dify
- 成功在终端显示文字和 DeepSeek 的回答

### 2026-7-26

#### 1. 配置 TTS
- 选择 MOSS—TTS-NANO
- 为避免影响已经运行成功的 voice-agent 环境，单独创建 moss-tts-nano 环境
- 使用 python 3.12
- 克隆 MOSS-TTS-Nano 项目
- 安装 requirements 等

#### 2. 测试 MOSS-TTS-NANO
- 模型成功生成 WAV 音频，并使用 Mac 自带的 afplay 命令播放

#### 3. 在 voice-agent 环境中调用 TTS
tts_client.py 主要完成：
- 接收需要合成的文字
- 调用 MOSS-TTS-Nano
- 使用 ONNX 后端生成回答音频
- 返回生成音频的文件路径
- 使用  afplay 播放音频
单独运行 tts_client.py 测试成功。

#### 4. 完整语音问答测试
目前完整流程为：
本地音频
-> SenseVoiceSmall 语音识别
-> 将识别结果发送给 Dify
-> DeepSeek 生成回答
-> MOSS-TTS-Nano 合成回答音频
-> afplay 自动播放

运行 voice_chat.py 后，程序能够依次完成：
1. 读取本地音频文件
2. 使用 SenseVoiceSmall 进行语音识别
3. 显示识别到的问题
4. 将问题发送给 Dify
5. 获取 DeepSeek 返回的回答
6. 显示 DeepSeek 的文字回答
7. 将回答发送给 MOSS-TTS-Nano
8. 生成回答音频
9. 自动播放回答音频

### 遇到的问题

#### 问题一
现象：使用 pip 安装 MOSS-TTS-Nano 的依赖时，`pynini` 编译失败。
报错信息：error: command '/usr/bin/clang++' failed with exit code 1
ERROR: Failed building wheel for pynini
原因：pip 尝试在 Mac 上从源码编译 `pynini`，但本地编译没有通过。
解决：使用 conda-forge 安装已经编译好的 `pynini`，避免在本地使用 clang++ 从源码编译。

#### 问题二
现象：安装 WeTextProcessing 时无法连接 GitHub。
第一次报错：Error in the HTTP2 framing layer
尝试将 Git 设置为 HTTP/1.1 后，再次出现：Failed to connect to github.com port 443
原因：当前网络连接 GitHub 不稳定，并不是 Python 包或项目代码本身的问题。
解决：不再直接从 GitHub 仓库安装，改为从 PyPI 安装 WeTextProcessing 的 wheel。
之后将 requirements.txt 中重复的 WeTextProcessing 安装项删除，再继续安装剩余依赖。

#### 问题三
现象：完整流程能够生成回答音频，但没有自动播放，终端中也没有显示“正在播放”。
排查：检查 voice_chat.py 后发现，文件中没有实际调用 play_audio()，运行的仍然是修改前的旧版本。
解决：重新修改并保存 voice_chat.py，加入：play_audio(answer_audio)
再次运行后，回答音频能够自动播放，完整流程成功。

### 当前结果
目前已经完成核心 Demo，能够通过一个 Python 程序完成从音频输入到语音回答的完整流程。


#### 4. 增加 Gradio 网页界面
- 安装 gradio
- 编写 app.py
- 进行简单的 UI 设计
- 在网页中显示 ASR 识别结果和 DeepSeek 回答
- 将 TTS 生成的回答音频返回网页播放器

### 遇到的问题

第一次测试时，ASR、Dify 和 TTS 都已经正常运行，但网页无法显示生成的音频。
报错信息：gradio.exceptions.InvalidPathError
原因：MOSS-TTS-Nano 生成的音频位于另一个项目目录，不在 Gradio 默认允许访问的当前目录或临时目录中。
解决：加入 allowed_paths=[str(moss_output_dir)]
修改后测试成功