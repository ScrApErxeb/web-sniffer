from bs4 import BeautifulSoup
import json

# -----------------------------
# HTML Parsing
# -----------------------------

def parse_html_title(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return soup.title.string if soup.title else ""

def parse_wikipedia(html: str, url: str = "") -> dict:
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string if soup.title else "No title"

    first_paragraph = ""
    content_div = soup.find("div", {"class": "mw-parser-output"})
    if content_div:
        for p in content_div.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                first_paragraph = text
                break

    return {"title": title, "url": url, "snippet": first_paragraph}

def parse_jeune_afrique(html: str, base_domain: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    for a in soup.select("article a"):
        title = a.get_text(strip=True)
        url = a.get("href")
        if title and url:
            if url.startswith("/"):
                url = f"{base_domain}{url}"
            articles.append({"title": title, "url": url, "snippet": ""})
    return articles

# -----------------------------
# JSON Parsing
# -----------------------------

def parse_google_results(json_data: dict) -> list[dict]:
    items = json_data.get("items", [])
    results = []
    for item in items:
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet", "")
        })
    return results

def parse_duckduckgo_results(raw_items: list[dict]) -> list[dict]:
    seen_urls = set()
    results = []
    for item in raw_items:
        title = item.get("title")
        url = item.get("href") or item.get("link")
        snippet = item.get("body") or ""
        if title and url and url not in seen_urls:
            results.append({"title": title, "url": url, "snippet": snippet})
            seen_urls.add(url)
    return results
