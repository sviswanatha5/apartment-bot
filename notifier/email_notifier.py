def notify(listings):

    print("\nNEW LISTINGS FOUND\n")

    for l in listings:
        print(f"[{l['site']}] ${l['price']} - {l['title']}")
        print(l["url"])
        print()