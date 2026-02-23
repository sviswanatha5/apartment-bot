from datetime import datetime, timedelta
import pandas as pd

from agents.craigslist_agent import fetch as fetch_craigslist
from agents.apartments_agent import fetch as fetch_apartments
from agents.zillow_agent import fetch as fetch_zillow

from core.filters import matches_filters
from core.storage import load_seen, save_seen
from notifier.email_notifier import notify


AGENTS = [
    fetch_craigslist,
    fetch_apartments,
    fetch_zillow
]


def is_recent(listing):

    if listing["posted_at"] is None:
        return True   # some sites don't expose post time

    cutoff = datetime.now(listing["posted_at"].tzinfo) - timedelta(days=1)
    return listing["posted_at"] >= cutoff


def main():

    seen = load_seen()
    seen_ids = set(seen["id"].values)

    all_results = []

    for agent in AGENTS:
        try:
            all_results.extend(agent())
        except Exception as e:
            print("Agent failed:", agent.__name__, e)

    filtered = []

    for l in all_results:
        if l["id"] in seen_ids:
            continue

        if not matches_filters(l):
            continue

        if not is_recent(l):
            continue

        filtered.append(l)

    if filtered:
        notify(filtered)

    if filtered:
        new_df = pd.DataFrame(filtered)
        combined = pd.concat([seen, new_df], ignore_index=True)
        save_seen(combined)


if __name__ == "__main__":
    main()