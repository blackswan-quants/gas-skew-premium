# Contributing

These are the BlackswanQuants programming guidelines applied to this repository. They are
strong recommendations rather than hard rules, but tooling enforces most of them, and
reviewers will ask about deviations.

## Workflow

1. Branch from an up-to-date `main`: `git switch main && git pull && git switch -c feat/<topic>`.
2. Commit small, focused changes with conventional messages (`feat: add TTF expiry calendar`).
3. Push the branch and open a pull request against `main`. CI must pass, and every review
   conversation must be resolved, before merging.
4. Delete the branch after merging.

Never commit market data, `.env` files or API keys. `.gitignore` covers the usual paths, and
pre-commit blocks files over 2 MB and private keys.

## Documentation and style

- **Docstrings:** NumPy style on every public function, with `Parameters`, `Returns`,
  `Raises`, and a `Notes` section explaining any decision that is not obvious.
- **Types:** full type hints with precise types (`pd.DataFrame`, `date`, dataclasses) rather
  than `Any`. Every module starts with `from __future__ import annotations`.
- **Lint and format:** ruff (PEP 8, docstrings, annotations) and `mypy --strict` run in
  pre-commit and CI, so style and type regressions are caught before review.

## Software design

- **No premature abstraction:** write explicit code. Handle Henry Hub and TTF directly rather
  than through a generic "market" object, until a third market justifies one.
- **Configuration:** settings come from `.env` through `gasskew.config.Settings`
  (pydantic-settings). A required API key is a field with no default, so a missing key fails
  at start-up.
- **Errors:** raise the domain exceptions in `gasskew.exceptions` (`DataFetchError`,
  `StaleDataError`, ...) for expected failures. Never raise or catch bare `Exception`.

## Correctness and testing

- **Invariants as code:** enforce financial and logical invariants with `assert` statements
  that fail loudly, not with comments. Examples: `extrinsic >= 0`, `bid <= ask`,
  `payoff - premium == pnl`.
- **Notebooks:** each research phase has an end-to-end notebook in `notebooks/` that asserts
  its numeric outputs against expected values.
- **Unit tests:** pytest tests in `tests/` isolate the maths, parsing and pipeline functions.
  Mark tests that need local market data with `@pytest.mark.data`, and long ones with
  `@pytest.mark.slow`.

## Data and time

- **D-1 discipline:** every pricing, classification and analysis function takes an explicit
  `as_of: date`, and its first step is `gasskew.temporal.filter_as_of(...)`
  (`trade_date <= as_of`). Never reference an implicit "today".
- **Checkpoints:** persist raw, parsed and validated stages as pickled DataFrames
  (`gasskew.checkpoints`), so each stage can be inspected and re-run without re-fetching data.
- **Outputs:** write result tables to the SQLite database at `Settings.db_path` for
  zero-setup inspection.

## Environment and reproducibility

- Python 3.12 with uv. Exact versions are pinned in `uv.lock`, so a clean checkout needs only
  `uv sync` and a `.env` file. Add dependencies with `uv add <pkg>` (or
  `uv add --dev <pkg>`) and commit the updated `uv.lock`.
- Run tools through `uv run` so everyone uses the same versions.

## Logging and presentation

- Every module uses `logger = logging.getLogger(__name__)`. No `print` outside the CLI and
  dashboards; ruff enforces this.
- Terminal output and progress bars use `rich`.
- Charts use Plotly, and raw-data browsing uses PySide6 table views (`uv sync --extra gui`).
- Polish matters: clear formatting, readable tables and thoughtful layout, not only correct
  numbers.
