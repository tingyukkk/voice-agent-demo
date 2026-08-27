from pathlib import Path
import subprocess


MOSS_PROJECT_DIR = Path.home() / "Projects" / "MOSS-TTS-Nano"
CONDA_EXE = Path.home() / "miniforge3" / "bin" / "conda"
OUTPUT_AUDIO = (
    MOSS_PROJECT_DIR
    / "generated_audio"
    / "moss_tts_nano_output.wav"
)


def synthesize_speech(text: str) -> Path:
    """调用 moss-tts-nano 环境，将文字合成为音频。"""

    text = text.strip()
    if not text:
        raise ValueError("需要合成的文字不能为空。")

    command = [
        str(CONDA_EXE),
        "run",
        "-n",
        "moss-tts-nano",
        "moss-tts-nano",
        "generate",
        "--backend",
        "onnx",
        "--prompt-speech",
        "assets/audio/zh_1.wav",
        "--text",
        text,
    ]

    result = subprocess.run(
        command,
        cwd=MOSS_PROJECT_DIR,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "MOSS-TTS-Nano 运行失败：\n"
            + result.stdout
            + result.stderr
        )

    if not OUTPUT_AUDIO.exists():
        raise FileNotFoundError(
            f"没有找到生成的音频：{OUTPUT_AUDIO}"
        )

    return OUTPUT_AUDIO


def play_audio(audio_path: Path) -> None:
    
    subprocess.run(
        ["afplay", str(audio_path)],
        check=True,
    )


def main():
    text = input("请输入需要合成的文字：").strip()

    print("正在合成语音……")
    audio_path = synthesize_speech(text)

    print(f"生成成功：{audio_path}")
    play_audio(audio_path)


if __name__ == "__main__":
    main()