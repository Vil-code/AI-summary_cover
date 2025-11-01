import os
import base64
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

from providers import get_items
from summarizer import summarize_article_text

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")


HF_IMG_MODEL = (
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
)


@app.get("/items")
def items():
    source = request.args.get("source", "books")
    query = request.args.get("q")
    try:
        items = get_items(source=source, query=query, limit=6)
        return jsonify(items), 200
    except Exception as e:
        return (
            jsonify(
                [
                    {
                        "title": "Error fetching items",
                        "source": "backend",
                        "url": "",
                        "description": str(e),
                    }
                ]
            ),
            200,
        )


@app.post("/summarize")
def summarize():
    data = request.get_json(force=True) or {}
    text = data.get("text")
    url = data.get("url")


    if text:
        summary = summarize_article_text(text)
        return jsonify({"summary": summary}), 200


    if url and "openlibrary.org" in url and "/works/" in url:
        try:
            json_url = url + ".json" if not url.endswith(".json") else url
            resp = requests.get(json_url, timeout=10)
            work = resp.json()
            desc = work.get("description")
            if isinstance(desc, dict):
                desc = desc.get("value", "")
            if not desc:
                desc = f"Book: {work.get('title', 'Unknown title')}"
            desc = desc[:1200]
            summary = summarize_article_text(desc)
            return jsonify({"summary": summary}), 200
        except Exception as e:
            return jsonify({"summary": f"Could not fetch book JSON: {e}"}), 200


    if url:
        try:
            resp = requests.get(url, timeout=10)
            page_text = resp.text[:1500]
            summary = summarize_article_text(page_text)
            return jsonify({"summary": summary}), 200
        except Exception as e:
            return jsonify({"summary": f"Could not fetch book page: {e}"}), 200

    return jsonify({"summary": "No text or URL to summarize."}), 200


@app.post("/cover")
def cover():

    if not HF_API_TOKEN:
        return jsonify({"error": "HF_API_TOKEN not set"}), 200

    data = request.get_json(force=True) or {}
    desc = (
        data.get("description")
        or data.get("text")
        or data.get("title")
        or "fantasy book cover"
    )

    prompt = (
        "high quality illustrated book cover, centered composition, trending on artstation, "
        "soft lighting, " + desc[:150]
    )

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    try:
        resp = requests.post(
            HF_IMG_MODEL,
            headers=headers,
            json={"inputs": prompt},
            timeout=60,
        )
    except Exception as e:
        return jsonify({"error": f"request to HF failed: {e}"}), 200

    if resp.status_code == 404:
        return jsonify(
            {
                "error": (
                    "HF image model not found (404). "
                    "Change HF_IMG_MODEL in backend/app.py to another public model, "
                    "e.g. 'stable-diffusion-v1-5/stable-diffusion-v1-5' or enable Inference API on the model page."
                )
            }
        ), 200

    if resp.status_code == 503:
        return jsonify({"error": "HF model is loading, please try again."}), 200

    if resp.status_code != 200:
        return (
            jsonify(
                {
                    "error": f"HF image error {resp.status_code}: {resp.text[:200]}",
                }
            ),
            200,
        )

    img_bytes = resp.content
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return jsonify({"image_base64": b64}), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)
