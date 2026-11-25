# Storage and drivers: data scan

Sources read on 21–25 Nov 2026. "Not verified" means we did not read it in a primary source.

## Summary

- **Load now:** EIA Lower 48 (original and latest values), AGSI+ for EU, NL and DE, and a daily US bill rate from the Fed H.15.
- **Keep for step 5:** CFTC positioning, NOAA degree days, ENTSOG flows, ALSI, EIA LNG exports.
- **Do not use:** FRED as a stored source (its terms forbid storing content without written consent) and analyst consensus (no free source passed our checks).
- **Main risk:** we found no AGSI+ first-print archive, and EU27 coverage reaches 100% only in 2023, so the EU "normal" before 2023 rests on partial or revised data.

## Timing convention

For series $i$, version $v$ and market $m$, the first usable trading day is

$$D(i,v,m)=\min\{d\in\mathcal C_m:\ \tau^{pub}_{i,v}+\delta\le\tau^{settle}_m(d)\}$$

$\mathcal C_m$ is the market's trading calendar, times are in UTC, and $\delta\ge 0$ is a declared margin. We compare against the **start** of the settlement window of that date. For explanatory tests any $\delta\ge 0$ is admissible; for trade simulations we use the next settlement. Local times are converted with `America/New_York` and `Europe/Amsterdam`.

- **As-of:** the time the value describes.
- **Published:** when that version became public.
- **First print:** the first published version.

Settlement windows:

| Market | Window | Source | Limit |
|---|---|---|---|
| Henry Hub futures | 14:28–14:30 ET; expiring month 14:00–14:30 ET | [NYMEX filing 19-198, Appendix B, PDF pp. 7-8, effective 3 Sep 2019 for trade date 4 Sep](https://www.cftc.gov/filings/orgrules/rule080819nymexdcm001.pdf), [CME page](https://cmegroupclientsite.atlassian.net/wiki/display/EPICSANDBOX/Natural+Gas) | Confirmed to 27 Aug 2025; no change found in NYMEX filings to 26 Oct 2026, but 2026 not read at CME |
| TTF futures | 17:05–17:15 CET | [ICE Endex Rules v1.66, App. B.1](https://www.ice.com/publicdocs/endex/ICE_Endex_Markets_B.V._Rules.pdf), [Circular E21/013](https://www.ice.com/publicdocs/endex/circulars/E21013.pdf) | In force on 30 Mar 2021 and in 2026; start date not found. ICE defines CET as CET or CEST as applicable (Rules, p. 19) |
| Henry Hub, holiday settlement | Energy settles at 13:30 ET on 24 Dec 2026 (time only, no window stated); no settlement on 26 Nov and 25 Dec | CME holiday PDFs, archived copies: [Christmas](https://web.archive.org/web/20261111062320/https://www.cmegroup.com/tools-information/holiday-calendar/files/2026/christmas-holiday-settlement-times-2026.pdf) (11 Nov 2026), [Thanksgiving](https://web.archive.org/web/2026/https://www.cmegroup.com/tools-information/holiday-calendar/files/2026/thanksgiving-holiday-settlement-times-2026.pdf) (22 Apr 2026) | Live CME files refuse automated access; "subject to change" |
| TTF, early settlement | 13:50–14:00 CET on 24 and 31 Dec 2026 | [Trading Schedule](https://www.ice.com/publicdocs/ICE_Endex_Trading_Schedule.pdf) | Windows must be stored by date |
| TTF option, expiry day | Reference price 13:50–14:00 CET from 23 Mar 2020; 17:00–17:15 before | [Circular 19/038](https://www.ice.com/publicdocs/endex/circulars/E19038.pdf) | Applies to expiring options only |

## EIA weekly storage

- **What:** working gas for Lower 48, East, Midwest, Mountain, Pacific, South Central (Salt, Nonsalt). [Report](https://ir.eia.gov/ngs/ngs.html), [notes](https://ir.eia.gov/ngs/notes.html)
- **Access:** report pages and public files. API v2 needs a free key; the route `natural-gas/stor/wkly` is not confirmed.
- **History:** five regions from 1 Jan 2010, with 2010 to 12 Jun 2015 reconstructed. The history file was [announced on 31 Aug 2015](https://ir.eia.gov/ngs/notice_08_31_2015.html); the five-region report began on 16 Nov 2015 at 3:00 pm for the week ending 6 Nov. [FAQ](https://ir.eia.gov/ngs/faqregions.html) Three-region archive: 31 Dec 1993 to 6 Nov 2015. [Notes](https://ir.eia.gov/ngs/notes.html)
- **Units:** Bcf.
- **As-of vs published:** Friday 09:00 CST as stated by EIA; standard release Thursday 10:30 ET. Exceptions move the day and the hour, e.g. Wed 25 Nov 2026 at 12:00 ET. [Schedule](https://ir.eia.gov/ngs/schedule.html) (2025–2027; earlier schedules survive in Wayback captures, of which we opened Jan 2014 and Jan 2020).
- **Five-year statistics:** daily linear interpolation between weekly values, then the same calendar day over the previous five years. Regional extremes do not necessarily sum to the Lower 48. [Methodology](https://ir.eia.gov/ngs/methodology.html)
- **Revisions:** published if the net change is at least 4 Bcf at regional or Lower 48 level (7 Bcf before Nov 2015). At least 10 Bcf in the two most recent weeks triggers an off-cycle release at 14:00 ET, excluding reclassifications, methodology changes and errors accumulated in earlier periods. [Policy](https://ir.eia.gov/ngs/revisions.html)
- **First prints:** [`revisions.xls`](https://ir.eia.gov/ngs/revisions.xls) holds original levels for 19 Jun 2015 to 10 Apr 2026 (565 weeks); [`archrevisions.xls`](https://ir.eia.gov/ngs/archrevisions.xls) covers 31 Dec 1993 to 28 Aug 2015 with old regions. Lower 48 originals differ from latest values in 69 of 565 weeks, by at most 14 Bcf; 15 of the 69 are below 4 Bcf, so that threshold must not be used to filter revisions.
- **Limits:** no revision dates, one row per week, no rows after 10 Apr 2026. For the history we need (1 Jan 2010 to 13 Nov 2026, 881 weeks) we compared the Lower 48 with reports or Weekly Updates of the time in 859 weeks, 44 of them through third-party copies: 858 match the assigned source, the exception is 13 Oct 2017 (report 3,646, file 3,645), and 22 weeks remain unchecked. In `revisions.xls`, South Central on 15 Jun 2018 is already revised (828, report 824). For the 31 weeks from 17 Apr to 13 Nov 2026, `ngshistory.xls` matches third-party copies of the reports on the Lower 48 (31 of 31) and on 210 of 211 regional and salt/nonsalt values. The exception (East, 2 Oct 2026: 812 against 862) is a typo in the AGA copy: its own weekly change and regional sum imply 862. These are not EIA originals, so the loader must flag them. Five-region values from 1 Jan 2010 to 12 Jun 2015 are labelled "Derived" and have no first print.
- **2015 break:** until 12 Jun 2015 the five-region Lower 48 differs from the latest three-region history by 0–2 Bcf, and from original estimates by up to 9 Bcf. From 19 Jun to 6 Nov 2015 it differs from what was published by up to 8 Bcf. From 19 Jun to 6 Nov `revisions.xls` equals the latest history, so it is not the three-region first print there. Use `archrevisions.xls` up to 28 Aug and [`archngshistory.xls`](https://ir.eia.gov/ngs/archngshistory.xls) from 4 Sep to 6 Nov 2015 (10 of 10 weeks match archived reports on the Lower 48, as do all 21 regional values available). The week of 13 Nov has only a five-region first print, released on 19 Nov, and it matches `revisions.xls`.
- **Cost:** free, public domain, cite EIA. [Reuse](https://www.eia.gov/about/copyrights_reuse.php)

## GIE AGSI+

- **What:** EU, country, company and facility levels. Fields: `gasInStorage`, `workingGasVolume`, `full`, `injection`, `withdrawal`, `status`, `updatedAt`. [API v013](https://www.gie.eu/transparency-platform/GIE_API_documentation_v013.pdf)
- **Access:** free, but the API requires registration and a personal key. Data may be used, repackaged and redistributed in any form, provided GIE or AGSI is credited as the source; we read this as covering our stored snapshots. Without the credit, GIE may withdraw the API key. [Data usage](https://agsi.gie.eu/data-usage)
- **History:** from 2011 where available. REMIT reporting from **7 Apr 2016**, complete only for operators GIE may publish. EU27 coverage was 98% on 8 Nov 2022 ([GIE Roundtable II](https://www.gie.eu/download/2022/GIE_TRA_ROUNDTABLE_II_018.pdf), slide 12), [99.85% targeted on 13 Mar 2023](https://www.gie.eu/press/gie-enhances-agsi-alsi-for-improved-gas-market-transparency/) and 100% by 1 Jun 2023 ([GIE Roundtable III](https://www.gie.eu/download/2023/230601_GIE_TRA_ROUNDTABLE_III_v2.pdf), slide 11). [Definitions](https://agsi.gie.eu/data-definition)
- **Units:** TWh (GCV, 25 °C) for stocks, GWh/d for flows, % for fullness. Fullness can briefly exceed 100%.
- **As-of vs published:** gas day runs 06:00–06:00 Italian time. Published at **19:30 and 23:00 CET**, for the gas day that ended that morning. API rows are dated by `gasDayStart`, so a row dated $D$ is published on $D+1$.
- **Late submissions:** operators missing 19:30 enter the 23:00 run. Flags: E, C, N. Missing or invalid data are replaced by system estimates (E), which carry into aggregates ([GIE Roundtable, 27 Apr 2022](https://www.gie.eu/download/2022/GIE_TRA_ROUNDTABLE_012.pdf), slide 23). The estimation method is not documented.
- **Revisions:** values may change without prior notice ([Disclaimer](https://agsi.gie.eu/disclaimer)); retroactive updates are announced in NEWS (GIE Roundtable, 27 Apr 2022, slide 23), but only larger corrections that operators report to GIE ([Roundtable II](https://www.gie.eu/download/2022/GIE_TRA_ROUNDTABLE_II_018.pdf), slide 25), so NEWS is not a full revision log. No vintage archive found. `updatedAt` is the last-touched time and gives no earlier values. **True first prints require a snapshot after the 19:30 run; a snapshot after 23:00 stores the 23:00 version, so we store both.**
- **EU targets:** [Reg. 2022/1032](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022R1032) set Member State targets of 80% by 1 Nov 2022 and 90% by 1 Nov from 2023, with exceptions. [Reg. 2025/1733](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32025R1733) allows 90% at any time from 1 Oct to 1 Dec, adds deviations, and extends Arts 6a–6d of Reg. 2017/1938 until 31 Dec 2027. This gives three regimes: before 1 Jul 2022, 1 Jul 2022 to 10 Sep 2025, and from 11 Sep 2025.
- **Cost:** free.

## US short rate

- **What:** 3-month Treasury bill, secondary market, discount basis. [H.15](https://www.federalreserve.gov/releases/h15/)
- **Access:** [H.15 XML](https://www.federalreserve.gov/releases/h15/data/FRB_h15_xml.zip), series `RIFSGFSM03_N.B` (tested). Data Download Program preformatted packages and saved URLs [are removed on 31 Mar 2027](https://www.federalreserve.gov/data/ddp-retirement-frequently-asked-questions.htm). FRED series `DTB3` is a useful reference, but its [terms](https://fred.stlouisfed.org/legal/) forbid storing content without the Bank's prior written consent.
- **History:** the series starts on 4 Jan 1954, so it covers the Henry Hub sample.
- **Units:** percent, 360-day discount basis. With quote $d_t$ in decimals and $n$ days to the bill's maturity, the bill's discount factor is $1-d_t n/360$. [31 CFR 356, App. B](https://www.law.cornell.edu/cfr/text/31/appendix-B_to_part_356) H.15 does not publish $n$.
- **As-of vs published:** quote at about 3:30 pm ([Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value_month=202611)). H.15 is posted Mon–Fri at 4:15 pm, no zone stated; we infer New York local time all year from file timestamps (16:15 EST on 24 Nov 2026, 16:15 EDT on 21 Sep 2026). The [feed](https://www.federalreserve.gov/feeds/Data/H15_H15_RIFSGFSM03_N.B.XML) always shows -05:00, so its offset must not be used. Day $d$ normally appears on the next publication day. Known late Treasury data: 13 Sep 2001 (11–12 Sep never published), 17 Sep 2018, 19 Aug 2020, 1 Aug and 12 Sep 2023; these notices do not name the bill series. Since 2010 the daily release was also postponed 13 times because the Board or federal offices were closed (e.g. 29–30 Oct 2012, 26 Dec 2014 published 29 Dec), so the publication calendar must come from the [H.15 announcements](https://www.federalreserve.gov/feeds/h15.html), not from "next weekday".
- **Revisions:** no routine policy found; occasional corrections and backfills. The XML is overwritten, so first prints require our own snapshots.
- **Cost:** free; Fed content is [public domain](https://www.federalreserve.gov/disclaimer.htm) with credit.
- **Assumption:** using a 3-month rate for every expiry approximates $D(t,T)$. For European options with the same expiry and premium paid upfront, parity gives a check, $\widehat D(t,T)=[(C_1-P_1)-(C_2-P_2)]/(K_2-K_1)$. With a futures-style premium $\widehat D=1$, so the check is uninformative there.
- **TTF:** the current [TFO option](https://www.ice.com/products/71085679/Dutch-TTF-Natural-Gas-Options-Futures-Style-Margin) has a futures-style premium. [Both styles coexisted in 2020](https://www.ice.com/publicdocs/endex/circulars/E20004.pdf), and TFM named the other style then: we must identify product and date in our data. Henry Hub: ON is American (PDF p. 47) and LN European (p. 53) ([NYMEX 21-201](https://www.cftc.gov/sites/default/files/filings/ptc/21/06/ptc062121nymexdcm005.pdf); codes in the table on p. 3); an upfront premium is inferred, not stated.

## Candidate drivers

| Driver | Measures | Freq. | History | As-of vs published | Revisions | Cost, access |
|---|---|---|---|---|---|---|
| [CFTC COT](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm), NYMEX natural gas, code 023651 (CFTC name "NAT GAS NYME"; not labelled Henry Hub) | Positions by trader type, incl. Managed Money | Weekly | 13 Jun 2006 (backcast) | Tue; Fri 15:30 ET; [holidays, shutdowns and incidents shift it](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalSpecialAnnouncements/index.htm) | Corrections; vintages not verified | Free, API without key |
| [ICE Endex COT](https://www.ice.com/publicdocs/CoT_and_Position_Reporting_2026.pdf), TTF code [TFM](https://www.ice.com/products/27996665/Dutch-TTF-Natural-Gas-Futures) | MiFID II positions, five categories | Weekly | COMB 2 Feb 2018 to 13 Nov 2026: 448 of 459 weeks (8 gaps in 2018, then 21 May 2021, 17 Nov 2023, 16 Oct 2026); FUTR only from 4 Sep 2026 | Usually Fri; ICE Wed 08:30 UK (09:30 CET); ESMA Thu 12:00 (time zone not stated); delays not verified | Republished automatically; 421 of 458 ESMA records are amendments and the first rows carry 2021 publication dates, so the register is not point-in-time; units vary (`OTHER`, `MWHO`) | Free to view: [ESMA register](https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_coder58) (PDF history); ICE Report Center (CSV/PDF) requires accepting its terms |
| [NOAA CPC](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/degree_days/) | US degree days, base 65 °F, weighted | Daily, weekly, monthly | [Folders](https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/) from 1981, not as-published | Not verified | Files rewritten; policy not verified | Free, no account |
| [NOAA forecasts](https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/) | 7-day degree-day forecasts | Daily | 2014–2026; as-issued at most from 13 Mar 2014 (inferred from timestamps) | Not verified | Not verified | Free, no account |
| [Copernicus ERA5](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) | Global reanalysis (we would subset Europe) | Hourly | From 1940 | About 5 days | ERA5T overwritten about 2 months after month end; final can differ | Account, token, licence acceptance |
| [ALSI](https://alsi.gie.eu/data-definition) | EU LNG stocks and send-out | Daily | 2012 where available; some operators from 7 Apr 2016 (API v013, p. 2) | 19:30 and 23:00 CET | Can change, no vintages found | Free, key |
| [ENTSOG](https://transparency.entsog.eu/) | Nominations, allocations, physical flows | Daily or hourly | Live API back to 2 Jan 2021 when tested on 23 Nov 2026 and to 1 Jan 2021 on 25 Nov (Physical Flow, daily; older requests return "more than 5 years old"); boundary rule not verified; older in TP Archives | `lastUpdateDateTime` is the upload time and rows are re-uploaded, so it is not a first-publication time | Provisional, Confirmed | API without key; 60 s per query, use small date windows; cite source and date. [Terms](https://transparency.entsog.eu/pdf/TRA0394_20161115_ENTSOG_TP_TC_of_Use_Rev_2_KNS_LG_KNS.pdf) |
| [EIA LNG exports](https://www.eia.gov/dnav/ng/ng_move_expc_s1_m.htm) | US exports by vessel | Monthly | "By Vessel" row listed from 2013, first non-zero May 2014; re-exports separate; total LNG from 1997 | About 2 months | Preliminary, then final | Free |
| Storage surprises | Reported change minus consensus | Weekly | None usable | Not applicable | Not applicable | Free-to-view forecasts exist, but none we checked combines a named source, timestamps and reuse rights; [Investing.com](https://www.investing.com/economic-calendar/natural-gas-storage-386) forbids storage without permission |

## First usable trading day

Assumes $\delta=0$ and the normal windows above, except where a row names a holiday. Local dates are the trading sessions of each market.

| Series | As-of | Published | Henry Hub | TTF |
|---|---|---|---|---|
| EIA, standard week | Fri 09:00 CST | Thu 10:30 ET | Thu | Thu |
| EIA, 25 Nov 2026 | Fri 20 Nov (by rule) | Wed 12:00 ET | Wed 25 (normal CME settlement, archived copy of Apr 2026) | Thu 26 |
| EIA, 24 or 31 Dec 2026 | Fri before (by rule) | Thu 10:30 ET (default rule: no December exception on the EIA schedule as of 19 Nov) | Thu (24 Dec: CME settles at 13:30 ET, still after 10:30; 31 Dec: normal times) | Mon 28 Dec or Mon 4 Jan (early settlement) |
| EIA, off-cycle revision | Revised week | 14:00 ET | Same day (on Henry Hub expiry, 14:00 is the start of the spot-month window); on 24 Dec 2026 (13:30 ET settlement) Mon 28 Dec | Next settlement |
| AGSI+, 23:00 run | Gas day ended that morning | 23:00 CET | Next settlement | Next settlement |
| ALSI, 23:00 run | Same | 23:00 CET | Next settlement | Next settlement |
| H.15 bill rate | Day $d$ | Next publication day, 4:15 pm ET | Next settlement after publication | Same, only if discounting is needed |
| CFTC COT, standard (live publication only; the 2006–2009 backcast came out in Oct 2009) | Tue | Fri 15:30 ET | Mon | Mon |
| CFTC COT, holiday weeks 2026 | Tue (by rule) | Mon 16 Nov, Mon 30 Nov, Mon 28 Dec, 15:30 ET (tentative schedule) | Next day (Tue 17 Nov, 1 Dec, 29 Dec) | Same |
| ICE Endex COT | Usually Fri | ICE Wed 09:30 CET; ESMA Thu 12:00 | Wed from ICE; Thu from ESMA | Wed from ICE; Thu from ESMA |
| EIA LNG exports | Month | About 2 months later | By release date | By release date |

Robustness: on normal days the standard rows are unchanged if the Henry Hub window starts at or after 14:00 and before 15:30 ET, and the TTF window at or after 16:30 and before 18:00 CET. This does not cover early-settlement days or a 12:00 ET release when US and EU clocks are out of step: it is then 17:00 in Amsterdam, before the TTF window (310 weekdays in 2010–2027).

Use actual release dates and date-specific windows, not the Thursday rule: EIA made a special release on [16 Nov 2015 at 3:00 pm](https://ir.eia.gov/ngs/faqregions.html), after the Henry Hub settlement. Where the actual date is unknown, the loader must flag it.

Holiday notes: ICE lists 26 Nov 2026 as an early close at 19:30 CET and 27 Nov at 21:00 CET, with no early settlement; [Trading Schedule](https://www.ice.com/publicdocs/ICE_Endex_Trading_Schedule.pdf). On normal days gas trades until 23:00 CET, after the settlement window (Rules v1.66, App. B.1, p. 168). CME (archived holiday PDFs, see Settlement windows): normal settlement on 25 and 27 Nov, none on 26 Nov; energy at 13:30 ET on 24 Dec, none on 25 Dec; normal times on 31 Dec (New Year's Eve PDF, archived 14 Nov 2026, listed on the [holiday calendar](https://www.cmegroup.com/tools-information/holiday-calendar.html)). EIA had not posted December exceptions on 19 Nov; in 2020, with the same calendar, it had added a Wed 23 Dec release at 12:00 ET by 17 Dec (Wayback copies of the schedule); the same in 2026 would move the TTF day to Thu 24. Recheck the schedule in mid-December.

## Recommendation

1. **EIA:** use Lower 48 as the main series and store `week_ending`, `published_at`, `original`, `latest`, `published_net_change` (first prints alone can misstate it: +93 instead of the published +103 Bcf on 23 Apr 2026). Flag weeks without a verified first print and snapshot each new report from now on.
2. **AGSI+:** use EU, NL and DE with a 23:00 CET cut-off. Snapshot both the 19:30 and 23:00 runs as soon as a key is available, and flag pre-April-2016 data and EU aggregates through 31 May 2023.
3. **Rate:** use the H.15 XML and keep FRED out of stored data.
4. **Normal level:** compute it only from data known at the time, and report results separately for the three EU target regimes.
5. **Timing:** store settlement windows by contract and date, and compute first usable days with real time zones.
6. **Drivers:** document now, load in step 5. CFTC and NOAA first, because they need no account.

## Not verified

- CME: settlement window in 2026 (no change found in NYMEX filings to 26 Oct 2026), ON settlement time (the table uses the futures window), LN/ON premium style (upfront inferred), official expiries; holiday settlement times read only in archived copies of CME PDFs (Thanksgiving copy from Apr 2026).
- ICE: start date of the 17:05 gas window, option version in our data, interest on margin. An [ESMA note](https://www.esma.europa.eu/sites/default/files/2025-05/ESMA74-2134169708-7942_ESMA_s_response_to_the_EC_commodity_derivatives_review.pdf) mentions a 2025 stop of TTF contracts offered in the UK; Endex TFM is still reported.
- AGSI+: summer meaning of "19:30 CET" before 2026 (archived summer-2026 pages show 19:30 CEST, i.e. local time).
- EIA: API route, 22 of 881 weeks since 2010 not compared with a report, EIA originals after 10 Apr 2026 (checked on third-party copies only), why `revisions.xls` stops at 10 Apr 2026, December 2026 release exceptions.
- H.15: time zone of the 4:15 pm posting (New York local inferred from file timestamps, not stated by the Fed).
- NOAA: publication times and revision policy. CFTC: vintages.
