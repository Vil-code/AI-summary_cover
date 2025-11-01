import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL_URL = (
    "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
)


def summarize_article_text(text: str) -> str:
    if not HF_API_TOKEN:
        return "HF_API_TOKEN not set on backend."

    text = text[:1200]

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 180,
            "min_length": 40,
            "do_sample": False,
        },
    }

    try:
        resp = requests.post(
            HF_MODEL_URL, headers=headers, json=payload, timeout=25
        )
    except requests.exceptions.ReadTimeout:
        return "Hugging Face endpoint was too slow (model may be loading). Try again."

    if resp.status_code == 503:
        return "Hugging Face model is loading — try again."
    if resp.status_code != 200:
        return f"HF API error {resp.status_code}: {resp.text[:200]}"

    data = resp.json()

    if isinstance(data, list) and data and "summary_text" in data[0]:
        return data[0]["summary_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]

    return "Could not read summary from Hugging Face."
