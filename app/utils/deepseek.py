import requests
import json

from app.config import DEEPSEEK_API_KEY


DEEPSEEK_URL = "https://openrouter.ai/api/v1/chat/completions"
# MODEL = "mistralai/mistral-7b-instruct"
MODEL = "openchat/openchat-7b"


async def chat(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    with requests.post(
        DEEPSEEK_URL, headers=headers, json=data, stream=True
    ) as response:
        if response.status_code != 200:
            print("Ошибка API:", response.status_code)
            return ""

        print(response.status_code)

        full_response = []

        for chunk in response.iter_lines():
            if chunk:
                chunk_str = chunk.decode("utf-8").replace("data: ", "")
                try:
                    chunk_json = json.loads(chunk_str)
                    if "choices" in chunk_json:
                        content = chunk_json["choices"][0]["delta"].get("content", "")
                        if content:
                            cleaned = process_content(content)
                            print(cleaned, end="", flush=True)
                            full_response.append(cleaned)
                except Exception:
                    pass

        return "".join(full_response)


def process_content(content):
    return content.replace("<think>", "").replace("</think>", "")
