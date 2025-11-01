import requests

OPENLIBRARY_SEARCH = "https://openlibrary.org/search.json"


def _fetch_work_description(work_key: str) -> str:
    try:
        resp = requests.get(f"https://openlibrary.org{work_key}.json", timeout=6)
        data = resp.json()
        desc = data.get("description")
        if isinstance(desc, dict):
            return desc.get("value", "")
        if isinstance(desc, str):
            return desc
    except Exception:
        pass
    return ""


def fetch_books(query: str | None, limit: int = 6):
    if not query:
        query = "bestseller"

    try:
        resp = requests.get(
            OPENLIBRARY_SEARCH,
            params={"q": query, "limit": limit},
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Open Library fetch failed:", e)
        return [
            {
                "title": "Example book (fallback)",
                "url": "https://openlibrary.org/",
                "source": "OpenLibrary",
                "description": "Could not fetch real books.",
            }
        ]

    items = []
    docs = data.get("docs", [])[:limit]

    for doc in docs:
        title = doc.get("title") or "Untitled"
        author = (
            ", ".join(doc.get("author_name", [])[:2])
            if doc.get("author_name")
            else "Unknown author"
        )
        work_key = doc.get("key")  # e.g. /works/OL45883W
        long_desc = ""
        if work_key:
            long_desc = _fetch_work_description(work_key)

        if not long_desc:
            long_desc = (
                doc.get("first_sentence", [""])[0]
                if doc.get("first_sentence")
                else f"{title} — a book by {author}."
            )

        items.append(
            {
                "title": title,
                "url": f"https://openlibrary.org{work_key}" if work_key else "",
                "source": author,
                "description": long_desc[:600],
            }
        )

    return items[:limit]


def get_items(source: str = "books", query: str | None = None, limit: int = 6):
    return fetch_books(query, limit=limit)
