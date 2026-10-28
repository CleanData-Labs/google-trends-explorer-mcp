# Node.js examples

Needs Node.js 18+ and an Apify API token.

```bash
npm install
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
node compare-keywords.mjs
```

| Script | What it does | Cost |
|---|---|---|
| `compare-keywords.mjs` | Compare several keywords on one Google Trends scale and print their averages. | 1 result = $0.0025. |
| `trending-now.mjs` | Print today's top Trending Now searches for a few countries. | 2 countries x 5 searches = 10 results = $0.025. |

Every script sets `maxTotalChargeUsd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
