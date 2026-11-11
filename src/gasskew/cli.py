"""Command-line entry point (``uv run gasskew ...``).

Pipeline phases (fetch, parse, calibrate, report) are added here as subcommands as
they are implemented; ``info`` is the environment smoke check.
"""

from __future__ import annotations

import logging
import platform

import typer
from rich.console import Console
from rich.table import Table

from gasskew import __version__
from gasskew.config import get_settings
from gasskew.log import setup_logging

app = typer.Typer(
    help="Natural gas implied-volatility skew premium (Henry Hub and TTF).",
    no_args_is_help=True,
)
console = Console()
logger = logging.getLogger(__name__)


@app.callback()
def _main() -> None:
    """Configure logging before any subcommand runs."""
    setup_logging(get_settings().log_level)


@app.command()
def info() -> None:
    """Print the package and Python versions and the resolved settings."""
    settings = get_settings()

    table = Table(title=f"gasskew {__version__}", header_style="bold cyan")
    table.add_column("setting")
    table.add_column("value")
    table.add_column("exists", justify="center")
    table.add_row("python", platform.python_version(), "")
    for label, path in (
        ("data_dir", settings.data_dir),
        ("checkpoint_dir", settings.checkpoint_dir),
        ("output_dir", settings.output_dir),
        ("db_path", settings.db_path),
    ):
        table.add_row(label, str(path), "yes" if path.exists() else "no")
    table.add_row("log_level", settings.log_level, "")
    console.print(table)


if __name__ == "__main__":
    app()
