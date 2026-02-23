import requests
from bs4 import BeautifulSoup
from core.normalize import make_listing_id

def fetch():

    url = "https://www.apartments.com/santa-clara-ca/"

    r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    })

    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for card in soup.select(".placard"):

        title_tag = card.select_one(".property-title")
        price_tag = card.select_one(".price-range")
        link_tag = card.select_one("a.property-link")

        if not title_tag or not price_tag or not link_tag:
            continue

        title = title_tag.text.strip()
        url = link_tag["href"]

        price_text = price_tag.text.replace("$","").replace(",","")

        try:
            low = int(price_text.split("–")[0])
            price = low
        except:
            continue

        listing = {
            "site": "apartments.com",
            "title": title,
            "price": price,
            "url": url,
            "location": "Santa Clara",
            "posted_at": None
        }

        listing["id"] = make_listing_id(
            listing["site"],
            listing["url"],
            listing["title"],
            listing["price"]
        )

        results.append(listing)

    return results