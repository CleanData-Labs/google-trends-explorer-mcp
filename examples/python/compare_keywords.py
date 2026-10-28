"""Compare several keywords on one Google Trends scale and print their averages.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python compare_keywords.py

Cost: 1 result = $0.0025.
The run is capped with max_total_charge_usd, so it cannot cost more than $0.25.
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "cleandata-labs/google-trends-explorer"
MAX_COST_USD = Decimal("0.25")

RUN_INPUT = {
    "keywords": [
        "chatgpt",
        "gemini",
        "claude"
    ],
    "compareKeywords": True,
    "geos": [
        "US"
    ],
    "timeRange": "today 3-m",
    "interestOverTime": True
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
        if item.get("type") != "interest_over_time":
            print("Skipped row:", item.get("type"), item.get("error", ""))
            continue
        print(f"{', '.join(item['keywords'])} in {item['geo'] or 'worldwide'}, {item['timeRange']}")
        for keyword, avg in (item.get("averages") or {}).items():
            print(f"  {keyword:<12} average {avg}")
        print("  last points:")
        for point in item["timeline"][-4:]:
            values = ", ".join(f"{k}={point[k]}" for k in item["keywords"])
            print(f"    {point['date']}: {values}")


if __name__ == "__main__":
    main()
