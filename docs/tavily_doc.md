Base URL + Auth

* Base URL: `https://api.tavily.com` (all endpoints) ([Tavily Docs][1])
* Auth: `Authorization: Bearer tvly-<YOUR_API_KEY>` (HTTP header, required for every endpoint) ([Tavily Docs][1])

# Endpoints

## POST /search — Tavily Search

Purpose: execute a web search tuned for LLM/agent use. ([Tavily Docs][2])
**Required body**

* `query` (string): the search query. ([Tavily Docs][2])

**Optional body (key ones)**

* `auto_parameters` (bool, default `false`): lets Tavily auto-tune parameters; uses 2 credits; you can still override explicitly. ([Tavily Docs][2])
* `topic` (`general`|`news`|`finance`, default `general`): category of search. ([Tavily Docs][2])
* `search_depth` (`basic`|`advanced`, default `basic`): `basic`=1 credit; `advanced`=2 credits and richer snippets. ([Tavily Docs][2])
* `chunks_per_source` (int, default 3, range 1–3): only when `search_depth=advanced`; controls snippets per source. ([Tavily Docs][2])
* `max_results` (int, default 5, range 0–20). ([Tavily Docs][2])
* `time_range` (`day|week|month|year` or short forms `d|w|m|y`): filter by publish/updated date. ([Tavily Docs][2])
* `start_date`, `end_date` (YYYY-MM-DD): absolute publish/updated date window. ([Tavily Docs][2])
* `include_answer` (boolean or `"basic"|"advanced"`, default `false`): include LLM-generated answer. ([Tavily Docs][2])
* `include_raw_content` (boolean or `"markdown"|"text"`, default `false`): include cleaned page content. ([Tavily Docs][2])
* `include_images` (bool, default `false`), `include_image_descriptions` (bool, default `false`). ([Tavily Docs][2])
* `include_favicon` (bool, default `false`). ([Tavily Docs][2])
* `include_domains` (string[], max 300) / `exclude_domains` (string[], max 150). ([Tavily Docs][2])
* `country` (enum of many country names; boosts that country; only with `topic=general`). ([Tavily Docs][2])

**Response (200)**

* `query`, optional `answer`, optional `images[]`, `results[]` (ranked), `response_time` (number), optional `auto_parameters{}`, `request_id` (string). ([Tavily Docs][2])

**HTTP status codes**: 200, 400, 401, 429, 432, 433, 500. ([Tavily Docs][2])

## POST /extract — Tavily Extract

Purpose: extract/clean content from one or more URLs. ([Tavily Docs][3])
**Required body**

* `urls` (string or string[]): URL(s) to extract. ([Tavily Docs][3])

**Optional body**

* `include_images` (bool, default `false`). ([Tavily Docs][3])
* `include_favicon` (bool, default `false`). ([Tavily Docs][3])
* `extract_depth` (`basic`|`advanced`, default `basic`): `basic`=1 credit / 5 successful URLs; `advanced`=2 credits / 5 successful URLs. Failed URLs don’t cost credits. ([Tavily Docs][3])
* `format` (`markdown`|`text`, default `markdown`). ([Tavily Docs][3])
* `timeout` (number seconds, 1–60; default: 10s for `basic`, 30s for `advanced` if unspecified). ([Tavily Docs][3])

**Response (200)**

* `results[]` (per URL: `url`, `raw_content`, optional `images[]`, optional `favicon`), `failed_results[]`, `response_time`, `request_id`. ([Tavily Docs][3])

**HTTP status codes**: 200, 400, 401, 429, 432, 433, 500. ([Tavily Docs][3])

## POST /crawl — Tavily Crawl  *(Beta)*

Purpose: graph-based crawler with built-in extraction and discovery. ([Tavily Docs][4])
**Required body**

* `url` (string): root/base URL. ([Tavily Docs][4])

**Optional body**

* `instructions` (string): natural-language guidance; when used, “mapping” cost doubles to 2 credits per 10 successful pages (vs 1/10). ([Tavily Docs][4])
* `max_depth` (int, default 1, range 1–5). ([Tavily Docs][4])
* `max_breadth` (int, default 20, ≥1). ([Tavily Docs][4])
* `limit` (int, default 50, ≥1): total pages to process. ([Tavily Docs][4])
* `select_paths` (string[] regex), `select_domains` (string[] regex). ([Tavily Docs][4])
* `exclude_paths` (string[] regex), `exclude_domains` (string[] regex). ([Tavily Docs][4])
* `allow_external` (bool, default `true`). ([Tavily Docs][4])
* `include_images` (bool, default `false`). ([Tavily Docs][4])
* `extract_depth` (`basic`|`advanced`, default `basic`): same credit logic as Extract (1 or 2 credits per 5 successful extractions). ([Tavily Docs][4])
* `format` (`markdown`|`text`, default `markdown`), `include_favicon` (bool, default `false`). ([Tavily Docs][4])

**Response (200)**

* `base_url`, `results[]` (per URL: `url`, `raw_content`, optional `favicon`), etc. ([Tavily Docs][4])

**HTTP status codes**: 200, 400, 401, **403**, 429, 432, 433, 500. ([Tavily Docs][4])

## POST /map — Tavily Map  *(Beta)*

Purpose: fast site mapping (discovery of URLs) with optional guidance. ([Tavily Docs][5])
**Required body**

* `url` (string): root/base URL. ([Tavily Docs][5])

**Optional body**

* `instructions` (string): guidance; increases cost to 2 credits per 10 successful pages (vs 1/10). ([Tavily Docs][5])
* `max_depth` (int, default 1, range 1–5), `max_breadth` (int, default 20, ≥1), `limit` (int, default 50, ≥1). ([Tavily Docs][5])
* `select_paths` (string[] regex), `select_domains` (string[] regex). ([Tavily Docs][5])
* `exclude_paths` (string[] regex), `exclude_domains` (string[] regex). ([Tavily Docs][5])
* `allow_external` (bool, default `true`). ([Tavily Docs][5])

**Response (200)**

* `base_url`, `results[]` (string URLs), `response_time`, `request_id`. ([Tavily Docs][5])

**HTTP status codes**: 200, 400, 401, **403**, 429, 432, 433, 500. ([Tavily Docs][5])

## GET /usage — Usage & limits snapshot

Purpose: returns current key usage, account plan usage/limits, and pay-as-you-go counters. ([Tavily Docs][6])
**Headers**: same Bearer token as above. ([Tavily Docs][6])
**Response (200)**

* `key`: `{ usage, limit }`
* `account`: `{ current_plan, plan_usage, plan_limit, paygo_usage, paygo_limit }` ([Tavily Docs][6])
  **HTTP status codes**: 200, 401. ([Tavily Docs][6])


[1]: https://docs.tavily.com/documentation/api-reference/introduction "Introduction - Tavily Docs"
[2]: https://docs.tavily.com/documentation/api-reference/endpoint/search "Tavily Search - Tavily Docs"
[3]: https://docs.tavily.com/documentation/api-reference/endpoint/extract "Tavily Extract - Tavily Docs"
[4]: https://docs.tavily.com/documentation/api-reference/endpoint/crawl "Tavily Crawl - Tavily Docs"
[5]: https://docs.tavily.com/documentation/api-reference/endpoint/map "Tavily Map - Tavily Docs"
[6]: https://docs.tavily.com/documentation/api-reference/endpoint/usage "Usage - Tavily Docs"
[7]: https://docs.tavily.com/documentation/rate-limits "Rate Limits - Tavily Docs"
