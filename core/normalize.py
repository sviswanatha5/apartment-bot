import hashlib

def make_listing_id(site, url, title, price):
    raw = f"{site}|{url}|{title}|{price}"
    return hashlib.sha256(raw.encode()).hexdigest()