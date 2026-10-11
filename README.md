<div align="center">

# Free Exchange Rate API

**Official central-bank exchange rates, keyless and free. No sign-up, no API key, no rate limit on the open endpoints.**

[![API status](https://img.shields.io/badge/API-online-brightgreen)](https://allratestoday.com/status)
[![Keyless check](https://github.com/AllRates-Today/free-exchange-rate-api/actions/workflows/check.yml/badge.svg)](https://github.com/AllRates-Today/free-exchange-rate-api/actions/workflows/check.yml)
[![Central banks](https://img.shields.io/badge/central%20banks-121-blue)](https://allratestoday.com/central-bank-rates-api/)
[![Tax authorities](https://img.shields.io/badge/tax%20authorities-3-blue)](https://allratestoday.com/tax-authority-rates-api/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**[Website](https://allratestoday.com/)** · **[Docs](https://allratestoday.com/docs/)** · **[Try it](https://allratestoday.com/api/open/central-bank/ecb?source=USD&target=EUR)** · **[Dataset on GitHub](https://github.com/AllRates-Today/central-bank-exchange-rates)**

</div>

---

## Overview

[AllRatesToday](https://allratestoday.com/) publishes the exchange-rate tables of **121 central banks and 3 tax authorities** (ECB, Federal Reserve, Bank of England, RBI, PBoC, HMRC, US Treasury, Swiss BAZG and more), each with the institution's own publication date. The **latest table of every institution is free and keyless**, served from Cloudflare's edge, with CORS open.

This repo is the front door to that free surface: what is keyless, what the responses look like, and drop-in replacements for the free APIs that have shut down or gone paid.

```bash
curl "https://allratestoday.com/api/open/central-bank/ecb?source=USD&target=EUR"
```

```json
{
  "bank": "ecb",
  "rate_date": "2026-10-09",
  "source": "USD",
  "target": "EUR",
  "rate": 0.8923790826,
  "rate_type": "reference",
  "derived": true,
  "method": "inverse",
  "stale": false,
  "cadence": "daily",
  "attribution": {
    "source": "Official rates published by ECB, served by AllRatesToday",
    "url": "https://allratestoday.com/central-bank-rates-api/ecb/",
    "terms": "Free to use with visible attribution linking to allratestoday.com"
  }
}
```

That's it. No sign-up, no key, no card.

## Table of contents

- [What is free](#what-is-free)
- [Quick start](#quick-start)
- [Keyless endpoints](#keyless-endpoints)
- [Drop-in replacements for dead or paid APIs](#drop-in-replacements-for-dead-or-paid-apis)
- [Static JSON on a CDN](#static-json-on-a-cdn)
- [AI agents and MCP](#ai-agents-and-mcp)
- [Code examples](#code-examples)
- [When you need a key](#when-you-need-a-key)
- [Terms](#terms)
- [License](#license)

## What is free

| | Keyless, free | Needs a free key |
|:--|:--|:--|
| Latest official table of any of the 124 institutions | ✅ | |
| One pair from that table (cross-computed inside the table, flagged `derived`) | ✅ | |
| ECB-based drop-in endpoints (Frankfurter, exchangeratesapi, Fixer, exchangerate.host shapes), **including dates and ranges** | ✅ | |
| Daily Reference Rate, one fixed mid-market table per business day (16:00 London) | ✅ | past dates |
| Commercial-bank counter boards (UAE, Vietnam, Sri Lanka, India, Indonesia, Armenia) | ✅ | |
| Hosted MCP server for AI agents | ✅ | |
| Dated central-bank tables, history series, cross-bank comparison, publication calendars | | 🔑 |
| Real-time mid-market rates for 160+ currencies | | 🔑 |

The free key gives 300 requests with no expiry and no card: [allratestoday.com/register](https://allratestoday.com/register). AI agents can self-issue a 100-call trial key without an account (see [AI agents and MCP](#ai-agents-and-mcp)).

## Quick start

Latest ECB table (about 30 currencies against EUR):

```bash
curl "https://allratestoday.com/api/open/central-bank/ecb"
```

One pair from any institution. The code is the institution's abbreviation, not a country code:

```bash
curl "https://allratestoday.com/api/open/central-bank/hmrc?source=GBP&target=USD"   # UK tax authority, monthly
curl "https://allratestoday.com/api/open/central-bank/fed?source=USD&target=JPY"    # Federal Reserve H.10
curl "https://allratestoday.com/api/open/central-bank/rbi?source=USD&target=INR"    # Reserve Bank of India
```

Every institution we carry, with its code and latest publication date:

```bash
curl "https://allratestoday.com/api/open/central-banks"
```

## Keyless endpoints

All open endpoints are `GET`, return JSON, allow any origin (CORS `*`), and are edge-cached.

| Endpoint | Returns |
|:--|:--|
| `/api/open/central-banks` | Every covered institution: `code`, `name`, `latest` publication date, `stale`, `cadence` |
| `/api/open/central-bank/{code}` | The institution's latest published table: `rate_date`, `rates[]` with `base`, `quote`, `type`, `value` |
| `/api/open/central-bank/{code}?source=X&target=Y` | One pair from that table; `derived: true` when cross-computed inside the table, `method` says how |
| `/api/open/reference-rate` | The latest Daily Reference Rate table ([methodology](https://allratestoday.com/reference-rate/)) |
| `/api/open/reference-rate?source=X&target=Y` | One pair from it |
| `/api/open/bank-rates/{country}` | Commercial-bank buy/sell boards for `ae`, `vn`, `lk`, `in`, `id`, `am`, next to the official rate |
| `/api/compat/{provider}/latest` | ECB table in another provider's response shape, see below |

Response fields worth knowing:

- `rate_date` is the institution's publication date. Cite it, not today's date.
- `stale: true` means the institution is behind its usual schedule. The last table is still served.
- `derived: true` means the pair was not published directly and was computed inside the same table (for example EUR/USD inverted to USD/EUR). `method` tells you which.
- `attribution` carries the terms: free use with a visible link back to allratestoday.com where rates are shown.

Base URL: `https://allratestoday.com`. Full reference: [allratestoday.com/docs](https://allratestoday.com/docs/#central-bank).

## Drop-in replacements for dead or paid APIs

If your code was written against one of these providers, change the host and keep the code. The data behind all four is the ECB daily reference table. Dates and date ranges work and are keyless.

| Your code used | Point it at |
|:--|:--|
| `api.frankfurter.app` / `api.frankfurter.dev` | `https://allratestoday.com/api/compat/frankfurter` |
| `api.exchangeratesapi.io` | `https://allratestoday.com/api/compat/exchangeratesapi` |
| `data.fixer.io/api` | `https://allratestoday.com/api/compat/fixer` |
| `api.exchangerate.host` | `https://allratestoday.com/api/compat/exchangerate-host` |

```bash
curl "https://allratestoday.com/api/compat/frankfurter/latest?from=USD&to=EUR,GBP"
curl "https://allratestoday.com/api/compat/frankfurter/2026-10-01?from=USD&to=EUR"
curl "https://allratestoday.com/api/compat/frankfurter/2026-09-01..2026-09-05?from=USD&to=EUR"
curl "https://allratestoday.com/api/compat/fixer/latest"
```

```json
{
  "amount": 1,
  "base": "USD",
  "date": "2026-10-09",
  "rates": { "EUR": 0.89237908, "GBP": 0.75640728 },
  "source": "European Central Bank reference rates, served by AllRatesToday"
}
```

Migration notes per provider: [allratestoday.com/migrate](https://allratestoday.com/migrate/).

## Static JSON on a CDN

If you would rather not call an API at all, the same official tables are committed daily to the [central-bank-exchange-rates](https://github.com/AllRates-Today/central-bank-exchange-rates) repo and served by jsDelivr. No request limits, no key, works from a browser or a spreadsheet.

```bash
curl -s https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/latest.json
```

```
=IMPORTDATA("https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/history/2026.csv")
```

The dataset is also mirrored on [Hugging Face](https://huggingface.co/datasets/AllRates/central-bank-exchange-rates) and [Kaggle](https://www.kaggle.com/datasets/allratestoday/central-bank-exchange-rates). The dataset is CC BY-NC 4.0; the API endpoints above are free for commercial use with attribution.

## AI agents and MCP

A hosted [MCP](https://modelcontextprotocol.io/) server runs at `https://allratestoday.com/api/mcp` (Streamable HTTP, stateless, keyless). Eleven tools: live and official rates, history, cross-bank comparison, publication calendars, the Daily Reference Rate, and `request_trial_key`, which lets an agent self-issue a 100-call, 7-day key with no account.

```json
{ "mcpServers": { "allratestoday": { "url": "https://allratestoday.com/api/mcp" } } }
```

For a local stdio server:

```bash
npx -y @allratestoday/mcp-server          # all tools
npx -y @allratestoday/central-bank-mcp    # official central-bank rates only
```

Trial keys can also be issued directly. The body must be JSON (a bodiless POST is rejected as a cross-site form):

```bash
curl -X POST https://allratestoday.com/api/agent/keys \
  -H "Content-Type: application/json" \
  -d '{"agent":"my-agent","purpose":"invoice FX"}'
```

Limits: 3 keys per IP per day, 100 calls per key, 7 days. Details: [allratestoday.com/docs#agent-keys](https://allratestoday.com/docs/#agent-keys) · [allratestoday.com/mcp](https://allratestoday.com/mcp/).

## Code examples

Runnable versions are in [`examples/`](examples/).

**JavaScript (browser or Node 18+)**

```js
const r = await fetch('https://allratestoday.com/api/open/central-bank/ecb?source=USD&target=EUR').then(r => r.json());
console.log(`1 USD = ${r.rate} EUR (ECB, ${r.rate_date})`);
```

**Python**

```python
import requests
r = requests.get("https://allratestoday.com/api/open/central-bank/ecb", params={"source": "USD", "target": "EUR"}).json()
print(f"1 USD = {r['rate']} EUR (ECB, {r['rate_date']})")
```

**PHP**

```php
$r = json_decode(file_get_contents('https://allratestoday.com/api/open/central-bank/ecb?source=USD&target=EUR'), true);
echo "1 USD = {$r['rate']} EUR (ECB, {$r['rate_date']})";
```

**Go**

```go
resp, _ := http.Get("https://allratestoday.com/api/open/central-bank/ecb?source=USD&target=EUR")
var r struct{ Rate float64 `json:"rate"`; RateDate string `json:"rate_date"` }
json.NewDecoder(resp.Body).Decode(&r)
fmt.Printf("1 USD = %v EUR (ECB, %s)\n", r.Rate, r.RateDate)
```

Per-bank zero-dependency npm packages exist for every institution, for example [`@allratestoday/ecb-exchange-rate`](https://www.npmjs.com/package/@allratestoday/ecb-exchange-rate). The full list is at [allratestoday.com/central-bank-rates-api](https://allratestoday.com/central-bank-rates-api/).

## When you need a key

Register at [allratestoday.com/register](https://allratestoday.com/register) for a free key with 300 requests, no card. It unlocks:

- the table any institution had in force on a **past date**, with weekend and holiday roll-back
- **history** series per pair, and CSV, XML and XLSX output on every table endpoint
- **cross-bank comparison** of one pair across every institution
- **real-time mid-market** rates for 160+ currencies

```bash
curl -H "Authorization: Bearer art_live_..." "https://allratestoday.com/api/v1/central-bank/ecb/2026-09-01?source=USD&target=EUR"
```

Paid plans start at €4.99 a month: [allratestoday.com/pricing](https://allratestoday.com/pricing/).

## Terms

- Open endpoints are free for any use, commercial included, with a visible "Rates by AllRatesToday" link where rates are shown.
- Official rates are the institutions' own published figures, served unchanged with their publication date. They are not live market quotes.
- The Daily Reference Rate is AllRatesToday's own calculation, not a registered benchmark. See the [methodology](https://allratestoday.com/reference-rate/) before using it contractually.
- Status page: [allratestoday.com/status](https://allratestoday.com/status). Data sources register: [allratestoday.com/data-sources](https://allratestoday.com/data-sources/).

## License

The examples in this repository are MIT licensed. The data is subject to the terms above.
