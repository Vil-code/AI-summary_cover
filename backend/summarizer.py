import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

HF_API_BASE = "https://router.huggingface.co/hf-inference/models"
HF_SUM_MODEL = "facebook/bart-large-cnn"
HF_SUM_URL = f"{HF_API_BASE}/{HF_SUM_MODEL}"

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}


def summarize_article_text(text: str) -> str:
    if not HF_API_TOKEN:
        return "HF_API_TOKEN not set on backend."

    text = text[:1200]

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 130,
            "min_length": 30,
            "do_sample": False,
        },
    }

    try:
        resp = requests.post(HF_SUM_URL, headers=HEADERS, json=payload, timeout=60)
    except Exception as e:
        return f"HF summarization network error: {e}"

    if resp.status_code != 200:
        return f"HF summarization error {resp.status_code}: {resp.text[:300]}"

    try:
        data = resp.json()
    except Exception as e:
        return f"HF summarization parse error: {e}"

    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            return first.get("summary_text") or first.get("generated_text") or str(first)
        return str(first)

    if isinstance(data, dict):
        return data.get("summary_text") or data.get("generated_text") or str(data)

    return str(data)
