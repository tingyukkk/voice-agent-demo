import os

import requests
from dotenv import load_dotenv


# 读取当前项目里的 .env 文件
load_dotenv()

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv(
    "DIFY_API_URL",
    "https://api.dify.ai/v1",
)


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
    return result["answer"]


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