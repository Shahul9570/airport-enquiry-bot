# chatbot/crawl_urls.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_internal(url, base_netloc):
    return urlparse(url).netloc == base_netloc or urlparse(url).netloc == ""

def get_all_links(start_url, limit=50):
    visited = set()
    to_visit = [start_url]
    collected_urls = []

    base_netloc = urlparse(start_url).netloc

    while to_visit and len(collected_urls) < limit:
        current = to_visit.pop(0)
        if current in visited:
            continue

        try:
            res = requests.get(current, timeout=10)
            visited.add(current)

            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, "html.parser")
            for link in soup.find_all("a", href=True):
                full_url = urljoin(current, link['href'])
                if is_internal(full_url, base_netloc) and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
                    collected_urls.append(full_url)

        except Exception as e:
            print("Error fetching:", current, "|", e)

    return list(set(collected_urls))[:limit]  # Limit to 50 to be safe

if __name__ == "__main__":
    changi_urls = get_all_links("https://www.changiairport.com/en.html", limit=50)
    jewel_urls = get_all_links("https://www.jewelchangiairport.com/en.html", limit=30)

    all_urls = changi_urls + jewel_urls
    print("✅ Total URLs collected:", len(all_urls))

    with open("data/urls.txt", "w") as f:
        for url in all_urls:
            f.write(url + "\n")
