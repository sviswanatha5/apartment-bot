
import requests
from bs4 import BeautifulSoup

def scrape_zillow():
    url = (
        "https://www.zillow.com/homes/for_rent/Santa-Clara-North-San-Jose_rb/"
        "2-_beds/3-_beds/pricea_sort/?searchQueryState={}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    listings = soup.find_all("article")  # this depends on Zillow HTML

    for l in listings:
        title = l.get_text()
        price = l.find("div", class_="list-card-price")

        if not price: 
            continue

        price_val = int(price.text.replace("$","").replace(",",""))
        if price_val <= 3200:
            results.append({
                "site": "Zillow",
                "title": title,
                "price": price_val,
                # parse url & date if possible
            })

    return results