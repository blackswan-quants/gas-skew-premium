# TTF data scan (ICE Endex via Databento `NDEX.IMPACT`)

Where each data need for the TTF leg of the Gas Skew Premium project lives in Databento's `NDEX.IMPACT`
dataset, when it is published, what it would cost, and how to bring the cost within budget.

**No data was purchased and no credit was spent.** Every number comes from free calls (`metadata.get_cost`,
`metadata.get_record_count`, `symbology.resolve`) or from the portal's cost estimate panel.
The exact queries behind every figure are in the appendix; the local scripts that ran them are not
committed, since they only call these free metadata endpoints.

---

## Cost revision after the second call

At the call I presented **2024 → today as feasible for ≈ $165** with `statistics` + `definition`.
After running further scripts **that estimate turned out to be too low**:

- the option settlements (`statistics`) had been quoted in a 19:30–20:00 Amsterdam window, but the end-of-day batch moves
  between ~19:10 and ~20:00 (§2): in summer it falls *before* 19:30, so many days were missed;
- re-quoted on a window that always contains the batch (18:30–21:00), option `statistics` on the **whole product** costs
  **$456.84** (2024 → today) instead of $124.92.

Because `statistics` and `definition` on the whole product turned out to be too expensive, **I quoted other schemas of the
same dataset as possible replacements (§5)** and **a selection of the option symbols** (first 3 expiries, delta filter).
The selection brings the original route back within budget: **≈ $49 for 2024 → today** (§5).

Decision recalled from the call: the Henry Hub vs TTF comparison is done on **2024 → today**; the 2021–22 crisis is covered by
a **snapshot of a few days** (§6.3), as for Henry Hub.

---

## 1. Where each need lives

| Need | Schema | Fields | First date |
|---|---|---|---|
| Daily settlement of every option strike | `statistics` | `stat_type = 3` → `price`; `ts_ref` = trading date; bit 0 of `stat_flags` = official | TFO 2019-03-03 |
| Strike, expiry, call/put, futures month | raw symbol (free) or `definition` | see below | TFO 2019-03-03 |
| Daily settlement of the futures months | `statistics` | `stat_type = 3` → `price` | TFM 2018-12-23 |
| Open interest per option | `statistics` | `stat_type = 9` → `quantity` | TFO 2019-03-03 |
| *(bonus)* ICE settlement IV and delta | `statistics` | `stat_type = 14`, `15` | TFO 2019-03-03 |

Stat types listed for `NDEX.IMPACT` in the Databento docs: 1, 2, 3, 4, 5, 6, 9, 11, 13, 14, 15.

**Option metadata without buying `definition`.** The raw symbol encodes everything:
`TFO FMZ0026_OMCE0000090002112626` = underlying futures Dec-2026 (`FMZ0026`), option (`O`), monthly (`M`), call (`C`),
European (`E`), strike `000009000` with `2` decimals = 90.00 EUR/MWh, expiry `112626` = 2026-11-26.
The list of raw symbols active on a given day is obtained **for free** with `symbology.resolve`
(`parent` → `instrument_id` → `raw_symbol`, both supported for `NDEX.IMPACT`). Tested on 2025-03-04: 7,707 active TFO
instruments, of which 4,594 single options decoded correctly; the others (e.g. `TFO   4  30901497`) are user-defined
strategies and are excluded.

**Size of the universe** (2024 → today, average per day): 8,564 TFO instruments; 851 single options in the first
3 expiries; 223 of those with delta ~0.1–0.9.

---

## 2. When the statistics are published

Record counts of `statistics` by hour and by 10 minutes (free `get_record_count`):

| Day | TFO options: end-of-day batch | TFM futures: pre-open snapshot | TFM futures: intraday |
|---|---|---|---|
| 2025-03-04 (winter) | **19:40** Amsterdam, 75,880 records | **07:00** Amsterdam, 20,412 records | continuous stream 07:00–18:00, peak ~17:20 |
| 2025-07-08 (summer) | **19:10** Amsterdam, 61,940 records | **07:00** Amsterdam, 19,065 records | continuous stream, peak ~17:30 |
| 2022-03-08 (crisis) | **19:50** Amsterdam, 159,380 records | **07:00** Amsterdam, 6,272 records | continuous stream, peak ~17:20 |

- **Options**: one batch per day at a variable time (19:10–20:00), ~7–8 records per option (one per stat type).
  It exists in 2022 too, about twice as large: pre-2024 `statistics` history is there.
- **Futures**: `statistics` is a continuous intraday stream (expensive during trading hours); the 07:00 pre-open snapshot is the
  cheap candidate for the previous day's settlement.
- Records are aligned on the trading date they refer to (`ts_ref`), not on publication time.

---

## 3. Costs of `statistics` + `definition` on the whole product

| Product | Selection | Schema | Variant | 2024 → today | 2019 → today | Method |
|---|---|---|---|---|---|---|
| TFO | whole product | `definition` | full day | $184.94 | $577.35 | exact |
| TFO | whole product | `definition` | 1 day per week | $31.04 | $95.71 | estimate |
| TFO | whole product | `statistics` | full day | $627.02 | $2,036.30 | exact |
| TFO | whole product | `statistics` | window 18:30–21:00 (end-of-day batch) | $456.84 | $1,716.38 | estimate |
| TFO | whole product | `statistics` | window 18:30–21:00, 1 day per week | $91.85 | $344.39 | estimate |
| TFM | whole product | `definition` | full day | $18.96 | $31.89 | exact |
| TFM | whole product | `statistics` | full day | $1,748.61 | $2,879.93 | exact |
| TFM | first 3 expiries | `definition` | 1 day per week | $0.00 | $0.01 | estimate |
| TFM | first 3 expiries | `statistics` | full day | $542.88 | $889.13 | estimate |
| TFM | first 3 expiries | `statistics` | window 07:00–08:00 (pre-open) | **$1.58** | $2.08 | estimate |
| TFM | first 3 expiries | `statistics` | window 17:10–17:45 (quoted and discarded) | $65.01 | $120.94 | estimate |
| TFM | first 3 expiries | `statistics` | window 17:00–18:00 (quoted and discarded) | $92.95 | $170.66 | estimate |

- **Options**: the end-of-day batch is ~75% of all option `statistics`, so a time window saves little; the cost depends on the
  **number of symbols** (§5).
- **Futures**: the afternoon windows fall inside the intraday stream and are discarded; the pre-open snapshot costs ~$2.
- "Estimate" = cost measured on a sample of business days (1 in 10; 1 week in 4 for `definition`) and scaled to all days.
- Downloading only some columns does **not** reduce the cost: Databento bills the volume of records of a schema, whose
  structure is fixed. Only fewer records (fewer symbols, shorter windows, fewer days, lighter schemas) reduce it.

---

## 4. Alternatives quoted (because `statistics` and `definition` on the whole product were too expensive)

### 4.1 Other schemas: what they contain and what they can replace

| Schema | What a record contains | What it can replace | What is lost compared with `statistics` |
|---|---|---|---|
| `trades` | every trade: price, size, timestamp, aggressor side | daily option price from trades | only strikes traded that day (sparse, stale wings); no open interest (volume instead); little data before 2024 |
| `tbbo` | every trade plus the best bid/ask at that moment | as `trades`, plus the spread at trade time | as `trades`; more expensive |
| `bbo-1m` | best bid and ask, one record per instrument per minute | daily mid = (bid + ask)/2; bid-ask spread | not official; no open interest; quotes on single options are uneven over time (§4.2) |
| `ohlcv-1d` | daily open, high, low, close, volume | futures close (first 3 expiries) | close ≠ settlement; for options it costs more than `trades` and contains less |

| Product | Selection | Schema | Variant | 2024 → today | 2019 → today | Method |
|---|---|---|---|---|---|---|
| TFO | whole product | `trades` | full day | $49.57 | $65.57 | exact |
| TFO | whole product | `tbbo` | full day | $82.62 | $109.29 | exact |
| TFO | whole product | `ohlcv-1d` | full day | $103.87 | $145.82 | exact |
| TFO | whole product | `bbo-1m` | window 16:50–17:00 | $31.54 | $32.14 | estimate |
| TFO | whole product | `bbo-1m` | window 17:15–17:30 | $61.96 | $62.86 | estimate |
| TFM | first 3 expiries | `ohlcv-1d` | full day | $2.27 | $6.07 | estimate |
| TFM | first 3 expiries | `bbo-1m` | window 17:15–17:30 | $0.41 | $1.08 | estimate |
| TFM | first 3 expiries | `trades` | full day (discarded) | $1,509.65 | $2,370.33 | estimate |

### 4.2 Selecting the option symbols (first 3 expiries, delta ~0.1–0.9)

For each sampled day: list of active options via `symbology.resolve` (free), strike and expiry read from the symbol, only
**monthly options of the 3 nearest expiries** kept; then, optionally, only strikes with **call delta N(d1) between 0.1 and 0.9**
(the "useful" part of the smile; put deltas in the same range in absolute value).

| Schema | Frequency | First 3 expiries | First 3 + delta 0.1–0.9 |
|---|---|---|---|
| `statistics` (evening batch) | every day | **$47.14** | $12.26 |
| `statistics` (evening batch) | 1 day per week | $9.48 | $2.47 |
| `trades` | every day | $16.04 | $5.24 |
| `bbo-1m` (17:15–17:30) | every day | $16.39 | $7.45 |

2024 → today; estimate on 76 sampled business days (1 in 10, all measured) scaled to 756.

Notes:
- **The delta filter is approximate in this quote**: the futures price is not free, so F is proxied by the median listed
  strike of each expiry and volatility is set to 60% (TTF second-month ATM implied vol was ~51–75% in 2024). In a real download
  the filter uses the actual daily futures price (≈ $2, §6) and a realised volatility, so a few strikes near the boundary may
  differ.
- **Quoted only for 2024 → today.** Before 2024 the approximations are not realistic (volatility well above 60% in 2021–22,
  median strike far from F after large moves), and 2024 → today is the period of the main analysis.
- **`bbo-1m` on single options is uneven**: $16.39 for the first 3 expiries against $61.96 for the whole product, so most quotes
  are on strategies; on some days single options have almost no quotes (e.g. 2025-03-04: a handful of records in 15 minutes),
  while the more recent part of the sample has more. A mid-price route based on `bbo-1m` cannot replace settlements on every day,
  but it is useful for bid-ask spreads (transaction costs).
- The selection can be applied when downloading: the request accepts an explicit list of raw symbols (up to 2,000 per request),
  rebuilt day by day.

---

## 5. Proposals

### 5.1 Main analysis, 2024 → today

| Proposal | What we buy | Total | Notes |
|---|---|---|---|
| **A – Daily settlements, first 3 expiries** *(recommended)* | TFO `statistics` evening batch, first 3 expiries, every day ($47.14) + TFM `statistics` 07:00, first 3 expiries ($1.58) | **≈ $49** | official daily settlement, open interest, ICE IV and delta for every strike of the first 3 expiries; daily futures price |
| **B – A + delta filter** | as A, options restricted to delta 0.1–0.9 ($12.26) + futures ($1.58) | **≈ $14** | cheapest daily option; requires the futures prices first to compute deltas |
| **C – Weekly settlements** | TFO `statistics`, first 3 expiries, 1 day per week ($9.48) + futures ($1.58) | **≈ $11** | weekly option prices, daily futures; enough for delta-hedged gains if positions open on weekly dates |
| **D – Trades** | TFO `trades`, first 3 expiries ($16.04) + TFM `ohlcv-1d` ($2.27) | **≈ $18** | only traded strikes; fallback if settlements are missing |

Optional add-on for transaction costs: TFO `bbo-1m` 17:15–17:30 on the first 3 expiries ($16.39; $7.45 with the delta filter)
and TFM `bbo-1m` ($0.41). Otherwise: futures hedge at 1 tick (€0.005/MWh) and a break-even analysis for option spreads.

**On `definition`.** It is not needed if the metadata decoded from the raw symbols (§1) match the official ones. This has been
checked by eye on a few catalogue examples, not systematically, so:
- **check at no extra cost**: the crisis snapshot (§5.3) already includes `definition` of all TFO options on five days ($2.35);
  the decoded strike, expiry, call/put and underlying can be compared instrument by instrument on those days;
- **optional insurance**: `definition` of the whole TFO product **once a week** ($31.04, 2024 → today), which also gives the
  exact expiry time and the official option → futures link (`underlying_id`).

| Proposal | Without `definition` | With weekly `definition` ($31.04) |
|---|---|---|
| A | ≈ $49 | ≈ $80 |
| B | ≈ $14 | ≈ $45 |

### 5.2 If the futures settlement is not in the 07:00 snapshot

Use TFM `ohlcv-1d` on the first 3 expiries ($2.27, daily close) or TFM `bbo-1m` 17:15–17:30 ($0.41, mid at settlement time).
The futures leg stays below $3 in every case.

### 5.3 Crisis snapshot (2021–22), a few days with full data

Full day, whole product, five key days: 2022-02-24 (invasion of Ukraine), 2022-03-07 (TTF intraday high),
2022-06-15 (Nord Stream flow cuts / Freeport LNG), 2022-08-26 (settlement high), 2022-09-27 (day after Nord Stream damage).
Dates to be aligned with the Henry Hub snapshot.

| Schema | TFO options | TFM futures | Total |
|---|---|---|---|
| `definition` | $2.35 | $0.05 | $2.40 |
| `statistics` | $9.37 | $8.82 | $18.19 |
| `trades` | $0.10 | $20.22 | $20.32 |
| `tbbo` | $0.16 | $33.71 | $33.87 |
| `bbo-1m` | $0.70 | $2.03 | $2.73 |
| `mbp-1` | $0.45 | $191.80 | $192.25 |

- In 2022 option prices on screen are almost absent (trades and book cost cents; `bbo-1m` is zero on 2022-08-26): option prices in
  the crisis come from **settlements**.
- Proposed package: **all option schemas ($13.13) + futures `statistics`, `bbo-1m`, `definition` ($10.90) ≈ $24** (exact).
  Minimum: option `statistics` + `trades` + futures `statistics` ≈ $18.

### 5.4 Total

| Package | 2024 → today | Crisis snapshot | Total |
|---|---|---|---|
| **A + snapshot** *(recommended)* | ≈ $49 | ≈ $24 | **≈ $73** |
| A + weekly `definition` + snapshot | ≈ $80 | ≈ $24 | ≈ $104 |
| A + snapshot + option spreads (`bbo-1m`) | ≈ $66 | ≈ $24 | ≈ $90 |
| B + snapshot | ≈ $14 | ≈ $24 | ≈ $38 |

All within the $125 free credit.

---

## 6. Open questions

1. **Test download** (fractions of a cent, needs approval): `statistics` for one option and one futures contract on one day, to
   confirm `stat_type` 3, 9, 14, 15 in the evening batch and the futures settlement in the 07:00 snapshot (`ts_ref`). The metadata
   decoded from the raw symbols are validated on the crisis-snapshot days, whose `definition` is already included.
2. **Crisis dates**: to be agreed with the Henry Hub snapshot.
3. **Frequency**: daily (A, B) or weekly (C) option observations, depending on the methodology for delta-hedged gains and smiles.

---

## 7. Contract terms that affect pricing

| Term | ICE rule | What it means for us |
|---|---|---|
| Exercise style | TFO options are European | Black-76 directly, no early exercise |
| Premium | Futures-style margin, not paid up front | No discounting: `C = F·N(d1) − K·N(d2)` |
| Settlement / exercise | Option exercises into the TFM futures of the same month; the futures delivers physically at TTF | Underlying of each option = same-month TFM contract |
| Expiry | Options: 5 calendar days before the delivery month (~14:00 CET). Futures: 18:00 CET, 2 UK business days before the delivery month | `T` is measured to the option expiry (Dec-26: option 2026-11-26, futures 2026-11-27) |
| Units | EUR/MWh; tick €0.005/MWh; strikes at least 5 above and below ATM in €0.50 steps | Prices and strikes in EUR/MWh; tick = minimum transaction cost |

Sources:
- ICE Endex Dutch TTF Natural Gas Options (Futures Style Margin): https://www.ice.com/products/71085679/Dutch-TTF-Natural-Gas-Options-(Futures-Style-Margin)
- ICE Endex Dutch TTF Natural Gas Futures: https://www.ice.com/products/27996665/Dutch-TTF-Natural-Gas-Futures
- Databento ICE Endex dataset (symbology, statistics flags): https://databento.com/docs/datasets/ndex-impact
- Databento statistics schema (stat types per dataset): https://databento.com/docs/schemas/statistics
- Databento symbology (free `symbology.resolve`, supported combinations): https://databento.com/docs/conventions/symbology
- Databento catalogue, TFO: https://databento.com/catalog/ndex/NDEX.IMPACT/options/TFO

---

## Appendix: exact queries

All calls on `dataset="NDEX.IMPACT"`, `end="2026-11-24"`, `start="2024-01-01"` or `"2019-03-03"`.

```python
c = databento.Historical()

# whole product, full day (summed over quarterly blocks)
c.metadata.get_cost(symbols="TFO.OPT" | "TFM.FUT", stype_in="parent", schema=<schema>, start=..., end=...)

# time windows: one request per sampled business day (1 in 10), scaled to all days
c.metadata.get_cost(symbols="TFO.OPT", stype_in="parent", schema="statistics",
                    start=<day 18:30 Europe/Amsterdam>, end=<day 21:00 Europe/Amsterdam>)

# futures, first 3 expiries: the three nearest monthly contracts of each sampled day
c.metadata.get_cost(symbols=["TFM FMZ0026!", "TFM FMF0027!", "TFM FMG0027!"], stype_in="raw_symbol",
                    schema="statistics", start=<day 07:00 Europe/Amsterdam>, end=<day 08:00 Europe/Amsterdam>)

# options, symbol selection (free): active options of a day, then cost of the selected list
ids = c.symbology.resolve(symbols=["TFO.OPT"], stype_in="parent", stype_out="instrument_id", start_date=<day>, end_date=<day + 1>)
raw = c.symbology.resolve(symbols=<ids>, stype_in="instrument_id", stype_out="raw_symbol", start_date=<day>, end_date=<day + 1>)
c.metadata.get_cost(symbols=<selected raw symbols, ≤ 2,000 per call>, stype_in="raw_symbol", schema="statistics",
                    start=<day 18:30 Europe/Amsterdam>, end=<day 21:00 Europe/Amsterdam>)

# crisis snapshot: full day, whole product
c.metadata.get_cost(symbols="TFO.OPT" | "TFM.FUT", stype_in="parent", schema=<schema>, start=<day>, end=<day + 1>)

# publication times
c.metadata.get_record_count(symbols="TFO.OPT" | "TFM.FUT", stype_in="parent", schema="statistics", start=<hour>, end=<hour + 1>)
```
