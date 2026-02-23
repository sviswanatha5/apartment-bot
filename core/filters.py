from config import MAX_PRICE, KEYWORDS

def matches_filters(listing):

    if listing["price"] is None:
        return False

    if listing["price"] > MAX_PRICE:
        return False

    text = f"{listing.get('title','')} {listing.get('location','')}".lower()

    if not any(k in text for k in KEYWORDS):
        return False

    return True