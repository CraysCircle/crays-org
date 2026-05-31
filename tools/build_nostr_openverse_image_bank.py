from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "nostr_openverse_image_bank.json"
USER_AGENT = "CraysNostrImageResearch/1.0 (+https://www.crays.org/nostr/)"
MAX_PAGES_PER_QUERY = 10


QUERY_GROUPS = {
    "start": [
        "technology laptop",
        "digital identity",
        "computer network",
        "open source software",
        "internet protocol",
        "cryptography",
        "developer desk",
        "web technology",
    ],
    "people": [
        "conference speaker",
        "software developer portrait",
        "community meetup",
        "hackathon people",
        "creator studio",
        "team collaboration",
        "public event audience",
        "workshop people",
    ],
    "apps": [
        "mobile app",
        "smartphone app",
        "user interface",
        "phone screen",
        "software dashboard",
        "web design",
        "mobile technology",
        "app development",
    ],
    "relays": [
        "server room",
        "data center",
        "network cable",
        "router network",
        "internet infrastructure",
        "computer servers",
        "fiber optic",
        "network switch",
    ],
    "nips": [
        "technical documentation",
        "software architecture",
        "whiteboard planning",
        "developer documentation",
        "code review",
        "engineering notes",
        "project planning",
        "technical standard",
    ],
    "crays": [
        "hospitality lounge",
        "hotel lobby",
        "business lounge",
        "event venue",
        "restaurant interior",
        "premium lounge",
        "city rooftop",
        "community event venue",
    ],
    "library": [
        "library research",
        "bookshelf",
        "archive documents",
        "reading room",
        "map research",
        "notebook desk",
        "research table",
        "books archive",
    ],
    "payments": [
        "bitcoin",
        "mobile payment",
        "payment terminal",
        "cash register",
        "digital wallet",
        "point of sale",
        "finance app",
        "payment phone",
    ],
    "creator": [
        "music studio",
        "podcast studio",
        "photography camera",
        "artist studio",
        "content creator",
        "video production",
        "creative workspace",
        "media studio",
    ],
    "privacy": [
        "cybersecurity",
        "privacy laptop",
        "secure technology",
        "lock computer",
        "encryption",
        "security camera",
        "password",
        "secure network",
    ],
}


def write_bank(existing: dict[str, dict]) -> None:
    images = sorted(existing.values(), key=lambda record: (record["keys"][0], record["title"].lower(), record["id"]))
    OUT.write_text(
        json.dumps(
            {
                "generated_at": "2026-05-31",
                "source": "Openverse API",
                "source_url": "https://api.openverse.org/v1/images/",
                "license_filter": "cc0,pdm",
                "note": "Images are used as public-domain/CC0 visual material where Openverse metadata reports cc0 or public domain mark. Each rendered Nostr page receives unique image URLs where the bank is large enough.",
                "images": images,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def is_good_result(item: dict) -> bool:
    if item.get("mature"):
        return False
    if item.get("category") not in {None, "photograph"}:
        return False
    license_name = str(item.get("license") or "").lower()
    if license_name not in {"cc0", "pdm"}:
        return False
    width = int(item.get("width") or 0)
    height = int(item.get("height") or 0)
    if width and height and (width < 640 or height < 420):
        return False
    url = item.get("url") or item.get("thumbnail")
    if not url or str(url).lower().endswith((".svg", ".gif")):
        return False
    return True


def main() -> None:
    existing: dict[str, dict] = {}
    if OUT.exists():
        for record in json.loads(OUT.read_text(encoding="utf-8")).get("images", []):
            existing[record["id"]] = record

    for key, queries in QUERY_GROUPS.items():
        for query in queries:
            for page in range(1, MAX_PAGES_PER_QUERY + 1):
                params = {
                    "q": query,
                    "page_size": 20,
                    "page": page,
                    "license": "cc0,pdm",
                    "mature": "false",
                    "category": "photograph",
                }
                url = "https://api.openverse.org/v1/images/?" + urlencode(params)
                try:
                    data = fetch_json(url)
                except Exception as exc:
                    print("skip", key, query, page, exc)
                    time.sleep(0.8)
                    continue
                results = data.get("results", [])
                if not results:
                    break
                for item in results:
                    if not is_good_result(item):
                        continue
                    image_id = str(item["id"])
                    record = existing.setdefault(
                        image_id,
                        {
                            "id": image_id,
                            "title": item.get("title") or query,
                            "creator": item.get("creator") or "",
                            "license": item.get("license") or "",
                            "license_version": item.get("license_version") or "",
                            "license_url": item.get("license_url") or "",
                            "source": item.get("source") or "",
                            "foreign_landing_url": item.get("foreign_landing_url") or "",
                            "url": item.get("url") or item.get("thumbnail"),
                            "thumbnail": item.get("thumbnail") or item.get("url"),
                            "width": item.get("width"),
                            "height": item.get("height"),
                            "keys": [],
                            "queries": [],
                        },
                    )
                    if key not in record["keys"]:
                        record["keys"].append(key)
                    if query not in record["queries"]:
                        record["queries"].append(query)
                print(key, query, page, "total", len(existing), flush=True)
                write_bank(existing)
                time.sleep(0.08)

    write_bank(existing)
    print("image bank", len(existing), "records", flush=True)


if __name__ == "__main__":
    main()
