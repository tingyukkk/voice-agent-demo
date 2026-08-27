from asr_client import transcribe_audio
from dify_client import ask_dify
from tts_client import synthesize_speech, play_audio


def main():
    audio_path = input("请输入音频文件名或路径：").strip()

    if not audio_path:
        print("音频路径不能为空。")
        return

    try:
        print("\n正在识别音频……")
        question = transcribe_audio(audio_path)

        print("\n识别到的问题：")
        print(question)

        print("\n正在调用 Dify……")
        answer = ask_dify(question)

        print("\nDify 回答：")
        print(answer)

        print("\n正在合成回答语音……")
        answer_audio = synthesize_speech(answer)

        print(f"\n回答音频已生成：{answer_audio}")
        print("正在播放……")
        play_audio(answer_audio)
        print("播放完成。")

    except Exception as error:
        print("\n运行失败：")
        print(error)


if __name__ == "__main__":
    main()