// Compare several keywords on one Google Trends scale and print their averages.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node compare-keywords.mjs
//
// Cost: 1 result = $0.0025.
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.25.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cleandata-labs/google-trends-explorer';
const MAX_COST_USD = 0.25;

const input = {
  "keywords": [
    "chatgpt",
    "gemini",
    "claude"
  ],
  "compareKeywords": true,
  "geos": [
    "US"
  ],
  "timeRange": "today 3-m",
  "interestOverTime": true
};

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
  process.exit(1);
}

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(input, { maxTotalChargeUsd: MAX_COST_USD });
console.error(`Run ${run.id} finished: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const item of items) {
  if (item.type !== 'interest_over_time') continue;
  console.log(`${item.keywords.join(', ')} in ${item.geo || 'worldwide'}, ${item.timeRange}`);
  for (const [keyword, avg] of Object.entries(item.averages ?? {})) {
    console.log(`  ${keyword.padEnd(12)} average ${avg}`);
  }
}
