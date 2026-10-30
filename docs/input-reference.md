# Input reference: Google Trends Scraper

Generated from the Actor's published input schema. All fields are optional unless marked required. The same fields are the arguments of the MCP tool `cleandata-labs--google-trends-explorer`.

Live version: <https://apify.com/cleandata-labs/google-trends-explorer/input-schema>

| Field | Type | Default | Description |
|---|---|---|---|
| `keywords` | array | `["chatgpt", "gemini"]` | Search terms to look up, e.g. ["chatgpt", "gemini"]. Each keyword is a separate query with its own 0-100 scale unless compareKeywords=true. Topic IDs such as "/m/0dl567" (from keywordSuggestions) also work. If you omit this field the default ["chatgpt","gemini"] is used, so pass [] when you only want trendingNowGeos or startUrls. |
| `startUrls` | array |  | Optional. Google Trends explore links, e.g. [{"url": "https://trends.google.com/trends/explore?q=bitcoin&geo=US"}]. Keywords, country, time range, category and property are read from each URL. Set keywords to [] to run only these URLs. |
| `keywordSuggestions` | boolean | `false` | true = also return Google Trends autocomplete topics for each keyword (title, type and topic ID such as "/m/0dl567"). Use a returned ID as a keyword for language-independent results. Default false. |
| `compareKeywords` | boolean | `false` | true = compare keywords on one shared 0-100 scale (groups of max 5, like trends.google.com). Use it for 'X vs Y' questions. false (default) = every keyword is scaled on its own, so values are not comparable between keywords. |
| `geos` | array | `["US"]` | Country or region codes, e.g. ["US"], ["GB","DE"] or ["US-CA"] for a US state. Each code is a separate query. [] = worldwide. Default ["US"]. |
| `timeRange` | string: `now 1-H` / `now 4-H` / `now 1-d` / `now 7-d` / `today 1-m` / `today 3-m` / `today 12-m` / `today 5-y` / `all` | `"today 12-m"` | Preset period: "now 1-H" past hour, "now 4-H" past 4 h, "now 1-d" past day, "now 7-d" past 7 days, "today 1-m" past 30 days, "today 3-m" past 90 days, "today 12-m" past 12 months (default), "today 5-y" past 5 years, "all" since 2004. Ignored when customTimeRange is set. |
| `customTimeRange` | string |  | Optional exact period that overrides timeRange. Format 'YYYY-MM-DD YYYY-MM-DD', e.g. '2024-01-01 2024-12-31'. |
| `category` | integer | `0` | Google Trends category ID to narrow ambiguous terms, e.g. 0 = all categories (default), 7 = Finance, 71 = Food & Drink, 958 = Jobs & Education. Use the number from the cat= parameter of a trends.google.com URL. |
| `property` | string: `web` / `youtube` / `news` / `images` / `froogle` | `"web"` | Which Google search to measure: "web" (default), "youtube", "news", "images" or "froogle" (Google Shopping). |
| `interestOverTime` | boolean | `true` | true (default) = return the 0-100 interest timeline for each query, plus averages and a partial-data flag. One result per query. |
| `interestByRegion` | boolean | `false` | true = also return interest per country / region / city for each query (see regionResolution). One result per query. Default false. |
| `regionResolution` | string: `""` / `COUNTRY` / `REGION` / `CITY` / `DMA` | `""` | Detail level for interestByRegion: "COUNTRY", "REGION" (state / province), "CITY" or "DMA" (US metro areas). Omit to let Google choose (countries for worldwide, regions inside one country). |
| `onlyRegionsWithData` | boolean | `true` | true (default) = drop regions where Google has no data, which keeps the output short. |
| `relatedQueries` | boolean | `false` | true = also return related search queries, top and rising (with growth % and 'Breakout' flag). Best for keyword research. One result per query. Default false. |
| `relatedTopics` | boolean | `false` | true = also return related topics, top and rising, with Knowledge Graph IDs. Google returns them only for single-keyword queries. One result per query. Default false. |
| `trendingNowGeos` | array |  | Optional country codes for today's Trending Now searches (Google's official RSS feed), e.g. ["US"] or ["GB","RO"]. Each trending search is one result. Set keywords to [] if you only want trending searches. |
| `trendingNowMaxItems` | integer (min 0) | `0` | Max Trending Now searches per country. 0 (default) = all items in Google's feed (usually 10-20). Use a small number such as 5 to keep the output short. |
| `language` | string | `"en-US"` | Interface language (hl parameter) for topic names and related queries, e.g. "en-US" (default), "de", "ro". |
| `timezoneOffset` | integer | `0` | Timezone offset in minutes, same as the tz parameter on trends.google.com, e.g. 0 = UTC (default), -120 = UTC+2. Affects hourly and daily timelines. |
| `delayBetweenRequestsSecs` | integer (min 0, max 30) | `1` | Pause between Google requests in seconds, 0-30. Default 1. Raise it only if many requests are retried. |
| `maxRetries` | integer (min 0, max 10) | `5` | Retries per request on rate limits or network errors, 0-10. Default 5. Each retry uses a new session (and proxy IP). |
| `requestTimeoutSecs` | integer (min 5, max 120) | `30` | Timeout per HTTP request in seconds, 5-120. Default 30. |
| `proxyConfiguration` | object | `{"useApifyProxy": true}` | Proxy settings. Default {"useApifyProxy": true}, which is recommended: Google rate-limits datacenter IPs and every retry rotates the IP. Leave as is unless you have a reason to change it. |
| `flattenOutput` | boolean | `false` | true = one row per date / region instead of one row with a nested array (handy for CSV and Sheets). Price is unchanged: one charge per data block. Default false, which is more compact for AI agents. |
