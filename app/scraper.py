import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

BAD_NAMES = {
    "Learn More",
    "Read More",
    "Assessments",
    "View",
    "Learn more",
    "Click Here"
}


def infer_test_type(name):

    lower = name.lower()

    if "personality" in lower:
        return "P"

    if "coding" in lower:
        return "T"

    if "technical" in lower:
        return "T"

    if "cognitive" in lower:
        return "C"

    if "simulation" in lower:
        return "S"

    if "behavioral" in lower:
        return "B"

    return "General"


def get_description(url):

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "lxml")

        paragraphs = soup.find_all("p")

        cleaned = []

        bad_phrases = [
            "We recommend upgrading",
            "Latest browser options",
            "Speak With Our Team",
            "Speak to Our Experts",
            "Cookie",
            "Accept cookies"
        ]

        for p in paragraphs[:10]:

            text = p.get_text(" ", strip=True)

            if len(text) < 40:
                continue

            skip = False

            for bad in bad_phrases:

                if bad.lower() in text.lower():
                    skip = True
                    break

            if not skip:
                cleaned.append(text)

        return " ".join(cleaned)[:1500]

    except Exception as e:

        print("Error scraping description:", e)

        return ""


def scrape_catalog():

    response = requests.get(
        BASE_URL,
        headers=headers
    )

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("Failed to fetch SHL catalog")
        return

    soup = BeautifulSoup(response.text, "lxml")

    links = soup.find_all("a")

    catalog = []

    seen = set()

    for link in links:

        href = link.get("href")
        name = link.get_text(strip=True)

        if not href or not name:
            continue

        if name in BAD_NAMES:
            continue

        if "/products/" not in href:
            continue

        full_url = (
            href if href.startswith("http")
            else f"https://www.shl.com{href}"
        )

        if full_url in seen:
            continue

        seen.add(full_url)

        print("Scraping:", name)

        description = get_description(full_url)

        item = {
            "name": name,
            "url": full_url,
            "description": description,
            "test_type": infer_test_type(name)
        }

        catalog.append(item)

        time.sleep(1)

    with open(
        "data/shl_catalog.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(catalog, f, indent=2)

    print(f"\nSaved {len(catalog)} assessments")


if __name__ == "__main__":
    scrape_catalog()