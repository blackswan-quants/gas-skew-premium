# gas-skew-premium

Investigates whether natural gas implied volatility, particularly the **upside wing**, is
overpriced in the **Henry Hub** (NYMEX) and **TTF** (ICE Endex) options markets.

> Status: project skeleton. Infrastructure, tooling and conventions are in place; data
> sources and research phases are added through pull requests.

## Quick start

```bash
# prerequisites: uv (https://docs.astral.sh/uv/) and git
uv sync                         # creates .venv with Python 3.12 + pinned deps from uv.lock
cp .env.example .env            # optional: override paths, add API keys
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run gasskew info             # smoke check: prints versions and resolved settings
uv run pytest                   # unit tests
```

Optional Qt table viewer for raw data: `uv sync --extra gui`.

## Data

Market data is **never committed**: it is vendor-licensed and large. Everything under
`data/` except the checkpoint folder is git-ignored. Each person keeps their own copy in
`data/` (or points `GASSKEW_DATA_DIR` elsewhere), and API keys live in `.env`.

| market | futures | options |
|---|---|---|
| Henry Hub | NYMEX NG | NYMEX LN / ON |
| TTF | ICE Endex TFM | ICE Endex TFO |

Sources, file names and schemas are documented here as loaders are added.

## Layout

```
src/gasskew/         library code, one module per concern
  config.py          pydantic-settings, reads .env (GASSKEW_* variables)
  exceptions.py      domain exceptions (DataFetchError, StaleDataError, LookAheadError, ...)
  temporal.py        filter_as_of: D-1 discipline for every pricing/analysis function
  checkpoints.py     pickled raw / parsed / validated stage checkpoints
  log.py             rich logging setup
  cli.py             `gasskew` CLI (typer); one subcommand per pipeline phase
tests/               pytest unit tests
notebooks/           end-to-end phase notebooks, each asserting its numeric outputs
scripts/             one-off utilities
data/                raw market data (git-ignored)
data/checkpoints/    generated stage pickles (git-ignored)
outputs/             figures, SQLite results DB, reports (git-ignored)
```

## How we work

- `main` is protected: every change, including the lead's, lands through a pull request
  with passing CI. Direct pushes and force-pushes are blocked.
- Branch from `main` with a conventional prefix, e.g. `feat/hh-option-loader`,
  `fix/ttf-expiry-calendar`, `docs/methodology`.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`). The commit-msg hook rejects
  anything else.
- Pre-commit runs ruff, mypy and the fast tests before every commit; CI runs the same
  checks on every pull request.

Coding standards are in [CONTRIBUTING.md](CONTRIBUTING.md).
