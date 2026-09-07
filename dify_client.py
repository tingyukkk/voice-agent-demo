import os
import re

import requests
from dotenv import load_dotenv


# 读取当前项目里的 .env 文件
load_dotenv()

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv(
    "DIFY_API_URL",
    "https://api.dify.ai/v1",
)


def clean_answer(answer: str) -> str:
    """移除回答开头的思考块，仅将正式回答交给界面和 TTS。"""
    if not isinstance(answer, str):
        raise RuntimeError("Dify 返回的回答不是文本。")

    text = answer.strip()
    while True:
        # Dify 的 reasoning 标记可能位于思考块内或紧邻其前后。
        marker = re.match(r"<!--dify[^>]*reasoning[^>]*-->", text, re.IGNORECASE)
        if marker:
            text = text[marker.end():].lstrip()
            continue
        opening = re.match(r"<think\s*>", text, re.IGNORECASE)
        if not opening:
            break
        closing = re.search(r"</think\s*>", text[opening.end():], re.IGNORECASE)
        if not closing:
            raise RuntimeError("Dify 的思考内容未完整结束，请重新提问。")
        text = text[opening.end() + closing.end():].lstrip()

    if not text:
        raise RuntimeError("Dify 没有返回正式回答，请重新提问。")
    return text


def ask_dify(question):
    """向 Dify 发送问题，并返回回答文字。"""

    if not DIFY_API_KEY:
        raise RuntimeError(
            "没有读取到 DIFY_API_KEY，请检查 .env 文件。"
        )

    response = requests.post(
        f"{DIFY_API_URL}/chat-messages",
        headers={
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "inputs": {},
            "query": question,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "tyra-python-demo",
        },
        timeout=60,
    )

    # 报错反馈
    if not response.ok:
        raise RuntimeError(
            f"Dify 请求失败：HTTP {response.status_code}\n"
            f"服务器返回：{response.text}"
        )

    result = response.json()
    return clean_answer(result["answer"])


def main():
    """直接运行本文件时，用于测试文字问答。"""

    question = input("请输入问题：").strip()

    if not question:
        print("问题不能为空。")
        return

    try:
        answer = ask_dify(question)

        print("\nDify 回答：")
        print(answer)

    except requests.RequestException as error:
        print("\n网络请求失败：")
        print(error)

    except (RuntimeError, KeyError) as error:
        print("\n程序运行失败：")
        print(error)


if __name__ == "__main__":
    main()