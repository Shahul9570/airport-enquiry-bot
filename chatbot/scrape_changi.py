# chatbot/scrape_changi.py

import requests
import trafilatura

def scrape_url(url):
    try:
        print(f"Scraping: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            content = trafilatura.extract(response.text)
            return content
        else:
            print(f"❌ Failed to fetch {url} (status code {response.status_code})")
            return None
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    with open("data/urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    all_text = []
    failed_urls = []

    for url in urls:
        content = scrape_url(url)
        if content:
            all_text.append(content.strip())
        else:
            failed_urls.append(url)

    print(f"\n✅ Total pages scraped successfully: {len(all_text)}")
    print(f"❌ Failed URLs: {len(failed_urls)}")

    with open("data/combined_text.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    with open("data/failed_urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(failed_urls))
