# Python examples

Needs Python 3.10+ and an Apify API token.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
python compare_keywords.py
```

| Script | What it does | Cost |
|---|---|---|
| `compare_keywords.py` | Compare several keywords on one Google Trends scale and print their averages. | 1 result = $0.0025. |
| `rising_queries_to_csv.py` | Save the rising and top related queries for a keyword to a CSV file. | 1 result per keyword = $0.0025 each. |
| `trending_now.py` | Print today's top Trending Now searches for a few countries. | 1 result per trending search: 2 countries x 5 = 10 results = $0.025. |

Every script sets `max_total_charge_usd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
