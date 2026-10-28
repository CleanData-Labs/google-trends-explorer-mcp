"""Save the rising and top related queries for a keyword to a CSV file.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python rising_queries_to_csv.py

Cost: 1 result per keyword = $0.0025 each.
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
        "electric bike"
    ],
    "geos": [
        "US"
    ],
    "timeRange": "today 12-m",
    "interestOverTime": False,
    "relatedQueries": True
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
    import csv

    rows = []
    for item in items:
        if item.get("type") != "related_queries":
            continue
        for kind in ("rising", "top"):
            for q in item.get(kind, []):
                rows.append({
                    "keyword": item["keyword"], "list": kind, "rank": q["rank"], "query": q["query"],
                    "value": q["value"], "growthPercent": q.get("growthPercent"),
                    "isBreakout": q.get("isBreakout", False),
                })
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", "related_queries.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "list", "rank", "query", "value",
                                               "growthPercent", "isBreakout"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    main()
