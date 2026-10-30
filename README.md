<p align="center"><img src="assets/icon.png" alt="Google Trends Scraper icon" width="96"></p>

# Google Trends Scraper (remote MCP tool)

Google Trends data for AI agents and scripts: interest over time, interest by region, related and rising queries, Trending Now and keyword suggestions. No Google API key.

It runs as an [Apify Actor](https://apify.com/cleandata-labs/google-trends-explorer) maintained by CleanData Labs, so you can use it in two ways:

1. **As a tool for your AI agent** (Claude, Cursor, VS Code / Copilot, Claude Code or any MCP client) through the hosted Apify MCP server. Nothing to install.
2. **From your own code** with the official `apify-client` for Python or JavaScript.

This repository holds the docs, ready-to-paste MCP configs and small runnable examples. The Actor itself is hosted on Apify; there is no server code to run here.

```text
https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer
```

## What it does

- **Interest over time**: the 0-100 timeline for one or more keywords, any country or US state, any period from the past hour to 2004-present, plus averages and a partial-data flag.
- **Compare keywords** on one shared scale (up to 5 per group, like trends.google.com) for "X vs Y" questions.
- **Interest by region**: country, region/state, city or US metro (DMA).
- **Related queries and topics**, top and rising, with growth % and the "Breakout" flag.
- **Trending Now**: today's trending searches per country from Google's official RSS feed, with approximate traffic and news links.
- **Keyword suggestions**: topic IDs (e.g. `/m/0dl567`) for language-independent queries.
- Search property: web, YouTube, News, Images or Google Shopping; category filter; or just paste trends.google.com explore URLs.

## Connect it to your AI agent (MCP)

The URL above is a Streamable HTTP MCP endpoint that exposes one tool, `cleandata-labs--google-trends-explorer`, whose arguments are the [input fields](docs/input-reference.md). Two ways to authorize:

- **OAuth (recommended):** add only the URL. On first use your client opens an Apify sign-in page. A free Apify account works.
- **API token:** send the header `Authorization: Bearer <YOUR_APIFY_TOKEN>`. Get the token in [Apify Console > Settings > API & Integrations](https://console.apify.com/settings/integrations). Keep it out of git.

Ready-made config files are in [`examples/mcp/`](examples/mcp/).

### Claude (claude.ai and Claude Desktop)

Settings > Connectors > **Add custom connector**. Name: `Google Trends Scraper`, Remote MCP server URL: `https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer`. Sign in with Apify when asked.

If you prefer a local config file, Claude Desktop can run Apify's official stdio server instead (`claude_desktop_config.json`, needs Node.js 18+):

```json
{
  "mcpServers": {
    "google-trends": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "cleandata-labs/google-trends-explorer"],
      "env": { "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>" }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project). OAuth:

```json
{
  "mcpServers": {
    "google-trends": {
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer"
    }
  }
}
```

With a token instead:

```json
{
  "mcpServers": {
    "google-trends": {
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer",
      "headers": { "Authorization": "Bearer <YOUR_APIFY_TOKEN>" }
    }
  }
}
```

### VS Code (GitHub Copilot agent mode)

`.vscode/mcp.json`. OAuth:

```json
{
  "servers": {
    "google-trends": {
      "type": "http",
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer"
    }
  }
}
```

With a token, VS Code can prompt for it once and store it securely:

```json
{
  "inputs": [
    { "type": "promptString", "id": "apify-token", "description": "Apify API token", "password": true }
  ],
  "servers": {
    "google-trends": {
      "type": "http",
      "url": "https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer",
      "headers": { "Authorization": "Bearer ${input:apify-token}" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http google-trends "https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer"
# or with a token:
claude mcp add --transport http google-trends "https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer" --header "Authorization: Bearer $APIFY_TOKEN"
```

### Other clients and combining tools

Any client that supports remote Streamable HTTP servers can use the same URL. To load several Actors in one connection, separate them with commas, e.g. `https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer,cleandata-labs/url-to-markdown`. Already using `https://mcp.apify.com` with the default tools? Ask your agent to run `cleandata-labs/google-trends-explorer`.

### Try these prompts

- "Is interest in electric bikes in the US growing or shrinking over the last 5 years? Show the yearly average."
- "Compare chatgpt, gemini and claude in the US over the past 90 days and tell me which one is rising fastest."
- "What are the rising Google searches related to 'air fryer' in the UK right now? Flag the breakouts."
- "What is trending on Google in Germany today? Give me the top 5 with their approximate search volume."

### Tips for agents

- Smallest useful input: `{"keywords": ["bitcoin"], "geos": ["US"]}` (one 12-month timeline, one result).
- Use `compareKeywords: true` whenever the user asks "X vs Y"; otherwise every keyword gets its own 0-100 scale and values are not comparable.
- Pass `keywords: []` when you only want `trendingNowGeos` or `startUrls`, otherwise the demo default `["chatgpt", "gemini"]` also runs.
- Every extra flag (`interestByRegion`, `relatedQueries`, `relatedTopics`) adds one result per query, so turn on only what you need.
- A typical run takes 5-10 seconds, usually inside the MCP call's default wait. The call returns a dataset ID; read the rows with `get-dataset-items`.

## Use it from code

Python (`pip install apify-client`):

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("cleandata-labs/google-trends-explorer").call(run_input={"keywords": ["chatgpt", "gemini", "claude"], "compareKeywords": True, "geos": ["US"], "timeRange": "today 3-m"})
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item)
```

JavaScript / Node.js (`npm install apify-client`):

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('cleandata-labs/google-trends-explorer').call({"keywords": ["chatgpt", "gemini", "claude"], "compareKeywords": true, "geos": ["US"], "timeRange": "today 3-m"});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

Runnable examples, each with a hard cost cap (`max_total_charge_usd` / `maxTotalChargeUsd`):

- Python: [`compare_keywords.py`](examples/python/compare_keywords.py), [`rising_queries_to_csv.py`](examples/python/rising_queries_to_csv.py), [`trending_now.py`](examples/python/trending_now.py). See [`examples/python/README.md`](examples/python/README.md).
- Node.js: [`compare-keywords.mjs`](examples/node/compare-keywords.mjs), [`trending-now.mjs`](examples/node/trending-now.mjs). See [`examples/node/README.md`](examples/node/README.md).

```bash
export APIFY_TOKEN=...            # never commit it
cd examples/python && pip install -r requirements.txt && python compare_keywords.py
cd examples/node && npm install && node compare-keywords.mjs
```

You can also call it over plain HTTP, from Make, Zapier or n8n, or on a schedule. See the [Apify API docs](https://docs.apify.com/api/v2).

## Input and output

Full list of input fields with types and defaults: [`docs/input-reference.md`](docs/input-reference.md).

Example output row:

```json
{
  "type": "interest_over_time",
  "keywords": [
    "electric bike",
    "e-scooter"
  ],
  "geo": "US",
  "timeRange": "today 12-m",
  "category": 0,
  "property": "web",
  "trendsUrl": "https://trends.google.com/trends/explore?q=electric+bike%2Ce-scooter&date=today+12-m&geo=US",
  "timeline": [
    {
      "date": "Oct 26 – Nov 1, 2025",
      "timestamp": 1761436800,
      "isPartial": false,
      "electric bike": 13,
      "e-scooter": 0
    }
  ],
  "averages": {
    "electric bike": 17,
    "e-scooter": 1
  },
  "pointCount": 53
}
```

Other row types: `interest_by_region` (`regions[]` with `geoCode`, `geoName` and one value per keyword), `related_queries` / `related_topics` (`top[]` and `rising[]` with `rank`, `value`, `growthPercent`, `isBreakout`), `trending_now` (`rank`, `title`, `approxTraffic`, `news[]`), `keyword_suggestions` and `error`.

## Pricing

Pay per event on Apify: **$0.0025 per result** ($2.50 per 1,000 results). You pay Apify from your own Apify account; nothing is billed through this repository.

- One result = one complete data block: the full timeline for a keyword set, the full region table, the related-queries list for one keyword, the suggestions for one keyword, or one Trending Now search.
- `flattenOutput: true` splits a block into many rows (handy for CSV) but it is still charged as one result.
- Error rows and `noData` rows (Google has nothing for that keyword/country/period) are free.
- Apify adds its standard Actor start event ($0.00005 per run). There is no separate compute or proxy fee.
- The smallest *maximum cost per run* you can set for this Actor is $0.25. The run stops cleanly when the limit is reached.

Apify's free plan includes a monthly platform credit (currently $5), which is enough to try the tool on real data. Prices can change; the [Actor page](https://apify.com/cleandata-labs/google-trends-explorer) always shows the current price.

## Good to know

- This is an independent tool by CleanData Labs. It is not affiliated with or endorsed by Google. It reads publicly available pages; use the data in line with the source site's terms and the laws that apply to you.
- The examples call the live Actor, so each run costs a little (see the cost note at the top of each script).
- Found a bug or need a field? Open an issue here or on the Actor's Issues tab on Apify.

## Links

- Apify Actor: <https://apify.com/cleandata-labs/google-trends-explorer>
- MCP endpoint: `https://mcp.apify.com?tools=cleandata-labs/google-trends-explorer`
- MCP registry name: `io.github.CleanData-Labs/google-trends-explorer` (see [`server.json`](server.json))
- Tutorial: [How to export Google Trends data to CSV/JSON without an API key (2026)](https://dev.to/cleandatalab/how-to-export-google-trends-data-to-csvjson-without-an-api-key-2026-2iea)
- Apify MCP server docs: <https://docs.apify.com/platform/integrations/mcp>

More tools from CleanData Labs:

- [URL to Markdown Converter](https://github.com/CleanData-Labs/url-to-markdown-mcp): Turn web pages and PDFs into clean, LLM-ready Markdown with metadata, token counts and optional RAG chunks.
- [Google Ads Transparency Scraper](https://github.com/CleanData-Labs/google-ads-transparency-explorer-mcp): See the ads any company runs on Google Search, YouTube, Shopping, Maps and Play, from the public Google Ads Transparency Center.
- [Keyword Research Tool — Autocomplete & Trends](https://github.com/CleanData-Labs/seo-keyword-research-for-agents-mcp): Keyword ideas from Google Autocomplete plus Google Trends interest, direction and rising searches, returned as one compact JSON result per seed keyword with a plain-English summary.

## License

The example code and docs in this repository are released under the [MIT License](LICENSE). The hosted Actor is a paid service under [Apify's terms](https://apify.com/store-terms-and-conditions).
