// Print today's top Trending Now searches for a few countries.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node trending-now.mjs
//
// Cost: 2 countries x 5 searches = 10 results = $0.025.
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.25.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cleandata-labs/google-trends-explorer';
const MAX_COST_USD = 0.25;

const input = {
  "keywords": [],
  "trendingNowGeos": [
    "US",
    "GB"
  ],
  "trendingNowMaxItems": 5
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

for (const item of items.filter((i) => i.type === 'trending_now')) {
  console.log(`${item.geo} #${item.rank} ${item.title} (~${item.approxTraffic} searches)`);
}
