# Henry Hub: data scan

Sources read on 25 Nov 2026. Costs are Databento's own quotes from free metadata calls, made on 25 Nov 2026; no credit was spent and nothing was bought. "Not verified" means we did not read it in a primary source.

## Summary

- **Where:** everything we need is in one Databento dataset, `GLBX.MDP3` (CME Globex), from **6 Jun 2010**: NG futures (`NG.FUT`), ON American options (`ON.OPT`) and LN European options (Globex code **LNE**, `LNE.OPT`).
- **Core route:** `statistics` (daily settlement, open interest, cleared volume) plus `definition` (strike, expiry, call/put, underlying future). `statistics` for every expiry of all three products costs $95 from 2010.
- **Top of book:** the full day is out of reach (about $10,800 from 2015 for the options). One snapshot per day at the settlement minute is affordable.
- **Proposal, within the $125 free credit:** settlements and open interest for the first 3 option expiries from 2015, trades with their side, and a daily top-of-book snapshot at the settlement minute from July 2021. Estimated total **$113–125**; see [Recommendation](#recommendation).
- **Main risk:** CME does not publish a settlement on the feed for an instrument **with no open interest and no volume**, so the far wings can be missing on some days. How often is a week-3 question.

## Where each need lives

All rows: dataset `GLBX.MDP3`, parent symbology (`stype_in="parent"`), so one symbol covers every expiry and strike of a product.

| Need | Schema | Field or record | Notes |
|---|---|---|---|
| Daily settlement, every option strike, calls and puts | `statistics` on `LNE.OPT`, `ON.OPT` | `stat_type` 3 (settlement price); `stat_flags` bit 0 final vs preliminary, bit 1 actual vs theoretical | First published shortly after the settlement window; use the final message. Not published for instruments without open interest or volume. [Databento, GLBX.MDP3](https://databento.com/docs/venues-and-datasets/glbx-mdp3) |
| Strike, expiry, call/put, futures month | `definition` | `strike_price`, `expiration`, `instrument_class`, `underlying` | Catalogue example: `ONZ6 C3650`, expiry 24 Nov 2026, underlying `NGZ26`; `LNEF7 C4500`, expiry 28 Dec 2026, underlying `NGF27`. [ON](https://databento.com/catalog/cme/GLBX.MDP3/options/ON), [LNE](https://databento.com/catalog/cme/GLBX.MDP3/options/LNE) |
| Daily settlement of the underlying futures | `statistics` on `NG.FUT` | `stat_type` 3 | Same days and same feed as the options. Calendar spreads sit in the same parent and must be dropped with `definition`. |
| Open interest and volume per option | `statistics` | `stat_type` 9 (open interest), 6 (cleared volume) | Normally published on the next UTC date; Friday's on Sunday. Store them under the trade date `ts_ref`, not the publication date. |
| Top of book | `bbo-1m` (sampled each minute), `tbbo` (book just before each trade), `mbp-1` (every change) | bid/ask price and size | Before May 2017 the history comes from the older MDP 2 feed (no order-level data; top of book is available). |
| Trades with buy or sell side | `trades`, or `tbbo`, which includes each trade | `side` = aggressor (A, B or N) | Implied trades have side N. LNE trades before 2015 cost $0.00 (2 decimal places), so LN had almost no Globex trades then. Off-screen deals (blocks, EFRP via ClearPort): not verified whether they appear. |
| Implied vol and delta from the exchange | none | `stat_type` 14, 15 | Not published on `GLBX.MDP3` (only on the ICE datasets), so we compute our own. [Databento, statistics](https://databento.com/docs/schemas-and-data-formats/statistics) |
| History 2015 to today | all of the above | | `metadata.get_dataset_range`: every schema above starts on 6 Jun 2010 (only `mbo`, `cmbp-1` and `cbbo-*`, not needed, start on 21 May 2017). |

Weekly options (ON1–ON5, LN1–LN5) exist but are left out: the project uses monthly expiries.

## Contract terms

| Term | NG futures | ON options | LN options |
|---|---|---|---|
| Globex / clearing code | NG / NG | ON / ON | LNE / LN |
| Rulebook chapter | 220 | 370 | 560 |
| Underlying | Gas at Henry Hub | One NG futures month | One NG futures month |
| Unit | 10,000 MMBtu (Ch. 220 not read; consistent with 560.03) | One NG futures contract | 10,000 MMBtu (cash) |
| Price, tick | USD/MMBtu, $0.001 (= $10 per contract; to check in `definition`) | USD/MMBtu, $0.001 (370101.C) | USD/MMBtu, $0.001 on Globex (560101.C) |
| Exercise | – | **American**: any business day up to expiry (370101.G) | **European**, cash settled on expiry day (560.01) |
| On exercise | Physical delivery (not verified) | Long or short NG futures position (370101.B) | Cash: (NG settlement − strike) × 10,000, or zero, for a call; the reverse for a put (560.03) |
| Last trading day | 3rd last business day of the month before delivery | Business day before the NG expiry (370101.F) | One business day before the NG expiry (560.05) |
| Example (Dec 2026) | `NGZ26`: 25 Nov 2026 | `ONZ6`: 24 Nov 2026 | `LNEZ6`: 24 Nov 2026 |
| Premium | – | Paid upfront (inferred, not verified) | Paid upfront (inferred, not verified) |
| Settlement window | 14:28–14:30 ET; expiring month 14:00–14:30 ET | Not verified | Not verified |

Sources:
- ON and LN: [NYMEX submission 21-201 to the CFTC, 18 Jun 2021](https://www.cftc.gov/sites/default/files/filings/ptc/21/06/ptc062121nymexdcm005.pdf): code table p. 3, Chapter 370 PDF pp. 46–47, Chapter 560 PDF pp. 52–53. Strikes follow Rule 300.20 in both.
- NG expiry: CME states that Penultimate futures stop "1 business day prior to the termination of trading in the corresponding contract month for Henry Hub Natural Gas Futures", on the 4th last business day ([CME](https://cmegroup.com/markets/energy/natural-gas/natural-gas-penultimate.contractSpecs.html)), so NG stops on the 3rd last. EIA gives the same rule ([EIA](https://www.eia.gov/dnav/ng/TblDefs/ng_pri_fut_tbldef2.asp)). Databento lists `NGZ26` expiring 25 Nov 2026, which is the 3rd last business day of November (26 Nov is Thanksgiving).
- Settlement window: [NYMEX filing 19-198, App. B](https://www.cftc.gov/filings/orgrules/rule080819nymexdcm001.pdf), as cited in `docs/data/storage.md` (PR #5).
- We could not read the live CME rulebook pages, which refuse automated access; the CFTC filings hold the rule text.

What this means for pricing:
- **LN** pays $\max(F_T-K,0)$ in cash, with $F_T$ the NG settlement on the option's expiry day $T$. With the premium paid upfront this is exactly Black-76: $C=D(t,T)\,[F\,N(d_1)-K\,N(d_2)]$, with $D(t,T)$ from the short rate (`storage.md`, "US short rate").
- **ON** is American on a future, so it can be worth more than Black-76 when deep in the money. The difference is small for short expiries and near-the-money strikes but not zero when rates are 4–5%. LN fits our pricer directly; ON needs an early-exercise model or a check against LN at the same strike and expiry.
- **Time to expiry** runs to the option expiry, one business day before the future's. Front, second and third months are ranked by option expiry.

## Cost

USD, `metadata.get_cost`, all strikes and both calls and puts. Periods start on the first date and stop before the second: 2010 = 6 Jun 2010 to 1 Jan 2015; 2015 = 1 Jan 2015 to 24 Nov 2026; 2020 = 1 Jan 2020 to 24 Nov 2026; crisis = 1 Jul 2021 to 1 Jan 2023.

| Route | Schema | Products | 2010→2015 | 2015→today | 2020→today | Crisis | 2015→today, first 3 expiries (est.) |
|---|---|---|---|---|---|---|---|
| Settlements, OI, volume | `statistics` | NG + ON + LNE | 16.41 | 78.53 | 64.50 | 16.92 | 26–35 |
| Instrument terms, every day | `definition` | NG + ON + LNE | 35.80 | 90.79 | 56.44 | 12.43 | 22–26 |
| Trades | `trades` | ON + LNE | 2.00 | 10.23 | 7.02 | 0.93 | 7–8 |
| Top of book at each trade | `tbbo` | ON + LNE | 3.34 | 17.06 | 11.70 | 1.54 | 11–13 |
| Top of book, each minute, full day | `bbo-1m` | ON + LNE | 315 | 10,848 | 9,556 | 1,989 | 3,322–8,065 |
| Top of book, every change | `mbp-1` | ON + LNE | 392 | 19,229 | 17,969 | 5,037 | 8,747–17,140 |
| Futures trades | `trades` | NG | 262 | 465 | 299 | 59 | – |
| Futures top of book, each minute | `bbo-1m` | NG | 168 | 556 | 378 | 58 | – |

By product, 2015→today: `statistics` LNE 51.95, ON 20.81, NG 5.76; `definition` LNE 60.70, ON 14.16, NG 15.93. LNE carries 2–3 times the data of ON in every schema.

**Cheaper top of book: one snapshot a day.** `bbo-1m` for the last minute of the settlement window (14:29–14:30 ET; 19:29–19:30 UTC in winter, 18:29–18:30 in summer) on four sample days:

| Product | Cost per day: 1 Mar 2016 / 2 Mar 2020 / 1 Mar 2022 / 2 Nov 2026 | 2015→today, all expiries (est.) | First 3 expiries: share / cost (est.) |
|---|---|---|---|
| LNE | 0.010 / 0.063 / 0.081 / 0.129 | ~194 | 0.29–0.53 / 56–103 |
| ON | 0.012 / 0.024 / 0.042 / 0.055 | ~93 | 0.32–0.42 / 30–39 |
| NG | 0.004 / 0.005 / 0.004 / 0.005 | ~13 | – / 13 |

A 5-minute window is quoted at the same price as a 1-minute one, so one request has a minimum size, and this route needs one request per trading day.

Quoted directly for the first 3 expiries on 12 days from 1 Sep 2021 to 2 Nov 2026, the snapshot costs per day: LNE $0.013–0.056 (mean 0.030), ON $0.008–0.035 (mean 0.017), NG, all expiries, $0.003–0.007 (mean 0.005). Times the 1,408 weekdays from 1 Jul 2021 to 24 Nov 2026 (holidays included, so an overestimate), that gives about $42, $24 and $7: **$73 from July 2021**.

How the estimates are built:
- **Snapshot, all expiries:** the four daily costs are interpolated linearly by year, times 250 trading days.
- **First 3 expiries:** a parent quote covers every listed expiry (out to 2032). On sample weeks (4–10 Jan 2016, 6–11 Jan 2020, 3–8 Jan 2022, 2–7 Nov 2026) we listed the instruments with `symbology.resolve` (free) and read the expiry month from the symbol (`LNEF7 C4500` = January 2027). We kept the 3 nearest months, quoted those symbols only, and divided by the parent quote for the same week. The table applies the lowest and highest share to the 2015→today total. Shares: `statistics` LNE 0.23–0.31, ON 0.40–0.66; `definition` 0.07–0.28; `trades` and `tbbo` 0.57–0.93; `bbo-1m` 0.28–0.89; `mbp-1` 0.36–0.93. These are 2–4 weeks per cell, not a quote.
- **Monthly definitions:** strike, expiry and type do not change over an instrument's life, so one day per month (about 143 days since 2015) is enough. On 10 sample weekdays (2 Mar of each year), one day of `definition` cost about $0.02 for the three products together (at most $0.020 for LNE, $0.008 for ON and $0.005 for NG), so about **$3–4** since 2015. Strikes listed in the middle of a month must then be read from the symbol or from the next month's file.

Exact queries:

```python
import databento as db

client = db.Historical()  # key from DATABENTO_API_KEY

# one cell of the table
client.metadata.get_cost(
    dataset="GLBX.MDP3",
    symbols=["LNE.OPT"],          # or "ON.OPT", "NG.FUT"
    stype_in="parent",
    schema="statistics",          # or definition, trades, tbbo, bbo-1m, mbp-1
    start="2015-01-01",
    end="2026-11-24",
)

# first 3 expiries: list the instruments, keep the 3 nearest months, quote them
r = client.symbology.resolve(
    dataset="GLBX.MDP3", symbols=["LNE.OPT"], stype_in="parent",
    stype_out="instrument_id", start_date="2026-11-02", end_date="2026-11-07",
)
# keys of r["result"] are raw symbols such as "LNEF7 C4500"
client.metadata.get_cost(
    dataset="GLBX.MDP3", symbols=front3_symbols, stype_in="raw_symbol",
    schema="statistics", start="2026-11-02", end="2026-11-07",
)
```

## Licence

- Databento: no venue licence is needed for historical data, defined as more than 24 hours old, unless we redistribute it ([Databento, 2 Oct 2023](https://databento.com/blog/introduction-market-data-licensing)).
- The repo is public, so raw or per-instrument data never goes in it (already a project rule); notebooks and the report show aggregates only.
- Not verified: Databento's subscriber terms (the terms page did not load) and whether CME limits publishing derived figures, such as a smile chart, in a public report.

## Recommendation

A mix that fits the $125 of free credit on one account. Each item is quoted exactly before it is bought.

| # | What | Schema | Products and period | Cost (est.) | Why |
|---|---|---|---|---|---|
| 1 | Settlements, open interest, volume | `statistics` | ON and LNE first 3 expiries, all NG; from 2015 | $26–35 | One full smile per day: the core |
| 2 | Strike, expiry, call/put, underlying | `definition` | One day per month, from 2015 | $3–4 | What each instrument is |
| 3 | Trades with side and the quote just before | `tbbo` | ON and LNE first 3 expiries, from 2015 | $11–13 | Who buys the wings |
| 4 | Top of book at the settlement minute | `bbo-1m` | ON and LNE first 3 expiries, plus NG; from 1 Jul 2021 | ~$73 | Checks settlements against real quotes, crisis included |
| | **Total** | | | **$113–125** | |

1. **Order:** buy items 1 and 2 first ($29–39); run the week-3 data check; then buy 3 and 4 with what is left. If item 4 is quoted above the remaining credit, start it later than July 2021.
2. **Build smiles from LN:** it is European and cash settled, and it carries more data than ON. Use ON as a second source and a liquidity check.
3. **What we give up:** 2010–2014, settlements beyond the third expiry, quotes before July 2021 and during the rest of the day. Keeping 3 expiries also means month-by-month requests with explicit symbol lists, because symbols such as `LNEF7` recur every 10 years.
4. **With more budget** (to ask the club): the snapshot from 2015 ($100–155 in total) and `statistics` for every expiry from 2010 ($95).
5. **Do not buy:** full-day `bbo-1m` or `mbp-1` for the options ($10,800 and $19,200 from 2015), or NG trades and top of book ($465 and $556): the daily futures settlement in `statistics` is enough for the underlying and for daily realised vol.

## Open questions

- How often do far strikes have no settlement (no open interest, no volume)? Measured in the week-3 data check.
- Which of ON and LN holds more open interest by strike and year? Data volume points to LN; open interest will decide.
- Are blocks and other off-screen deals in `trades`? A check: compare Globex trade volume with cleared volume (`stat_type` 6) on a sample day. LNE had almost no Globex trades before 2015.
- Premium paid upfront for ON and LN, automatic exercise rules, and the options' settlement window: to confirm on the CME contract pages.
- Does the licence allow aggregated charts in a public repo and report?
- Can the club add budget beyond the $125 free credit, and does downloading the same data again cost again?
