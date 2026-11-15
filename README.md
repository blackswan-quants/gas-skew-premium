# gas-skew-premium

Is natural gas implied volatility, especially the **upside wing**, overpriced in **Henry Hub**
(NYMEX) and **TTF** (ICE Endex) options?

## Setup

```bash
git clone https://github.com/blackswan-quants/gas-skew-premium.git
cd gas-skew-premium
uv sync                  # Python 3.12 + exact tool versions (needs https://docs.astral.sh/uv/)
```

Before pushing, run the same checks as CI:

```bash
uv run ruff format .
uv run ruff check .
uv run mypy
```

## Data

From [Databento](https://databento.com): Henry Hub via `GLBX.MDP3`, TTF via `NDEX.IMPACT`.
Never committed: it is licensed and this repo is public. One downloader holds the API key and
saves files to the team's shared drive; everyone else reads from there.

## Roadmap

Each step lands as one or more pull requests, and the lead checks it before the next step
builds on it. Step 1 runs until mid-December; the rest from mid-February to the final report
at the end of May.

1. **data**: Henry Hub and TTF option settlements and futures (Databento), plus storage
   (EIA, AGSI+); coverage and quality checked before anything is built on them
2. **smiles**: Black-76 prices, implied vols, SVI fits and skew measures (risk reversal,
   butterfly, wing minus ATM) for each expiry
3. **skew premium**: model-free implied vs realised skewness at 30 days: does the skew realise?
4. **premia**: is variance overpriced, and is the upside wing rich relative to ATM?
5. **dynamics**: when and why: seasonality, co-movement with price and vol, storage,
   persistence, and how TTF differs from Henry Hub
6. **trades** (if time allows): do simple structures capture the premium after costs?
7. **report**: final report on the club template, end of May

Every headline result is reported with and without the 2021–22 crisis
(1 Jul 2021 to 31 Dec 2022).

## How we work

1. **Task**: the lead opens a GitHub issue for each task and assigns it to you. It says what
   to do and when it is done; ask questions in the issue.
2. **Branch**: in your clone, branch from an up-to-date `main`, named after the issue:
   `git switch main && git pull && git switch -c feat/12-hh-settlements`.
3. **Push**: commit following [CONTRIBUTING.md](CONTRIBUTING.md), then push the branch to this
   repo: `git push -u origin feat/12-hh-settlements`.
4. **Pull request**: open it against `main`, fill in the template and write `Closes #12`, so
   merging closes the issue. CI must pass.
5. **Review session**: walk the lead through every line; the lead approves and squash-merges.
