import requests
from bs4 import BeautifulSoup
from dateutil import parser
from core.normalize import make_listing_id

BASE_URL = "https://sfbay.craigslist.org"

def fetch():

    url = (
        "https://sfbay.craigslist.org/search/apa"
        "?query=santa+clara+san+jose"
        "&max_price=3200"
    )

    r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    })

    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for row in soup.select(".result-row"):

        title = row.select_one(".result-title").text.strip()
        link = row.select_one(".result-title")["href"]

        price_tag = row.select_one(".result-price")
        price = int(price_tag.text.replace("$","")) if price_tag else None

        time_tag = row.select_one("time")
        posted = parser.parse(time_tag["datetime"]) if time_tag else None

        hood = row.select_one(".result-hood")
        location = hood.text.strip(" ()") if hood else ""

        listing = {
            "site": "craigslist",
            "title": title,
            "price": price,
            "url": link,
            "location": location,
            "posted_at": posted
        }

        listing["id"] = make_listing_id(
            listing["site"],
            listing["url"],
            listing["title"],
            listing["price"]
        )

        results.append(listing)

    return results