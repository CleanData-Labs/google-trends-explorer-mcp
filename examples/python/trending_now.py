"""Print today's top Trending Now searches for a few countries.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python trending_now.py

Cost: 1 result per trending search: 2 countries x 5 = 10 results = $0.025.
The run is capped with max_total_charge_usd, so it cannot cost more than $0.25.
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "cleandata-labs/google-trends-explorer"
MAX_COST_USD = Decimal("0.25")

RUN_INPUT = {
    "keywords": [],
    "trendingNowGeos": [
        "US",
        "GB"
    ],
    "trendingNowMaxItems": 5
}


def run_actor(run_input: dict) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first "
                 "(Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=MAX_COST_USD)
    if run is None:
        sys.exit("The run could not be started.")
    print(f"Run {run.id} finished: {run.status}", file=sys.stderr)
    return list(client.dataset(run.default_dataset_id).iterate_items())


def main() -> None:
    items = run_actor(RUN_INPUT)
    for item in items:
        if item.get("type") == "trending_now":
            print(f"{item['geo']} #{item['rank']:<2} {item['title']}  (~{item['approxTraffic']} searches)")


if __name__ == "__main__":
    main()
