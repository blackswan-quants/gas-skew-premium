"""Structured, validated configuration loaded from environment variables / ``.env``."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_LEVELS: frozenset[str] = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


class Settings(BaseSettings):
    """Runtime settings for the gasskew pipeline.

    Values are read from environment variables prefixed with ``GASSKEW_`` or from a
    ``.env`` file in the project root. Relative paths are resolved against the root.

    Attributes
    ----------
    data_dir : Path
        Directory holding raw market data (Henry Hub and TTF futures and options).
    checkpoint_dir : Path
        Directory for pickled stage checkpoints (raw / parsed / validated).
    output_dir : Path
        Directory for figures, reports and the SQLite results database.
    db_name : str
        File name of the SQLite results database inside ``output_dir``.
    log_level : str
        Logging level name.

    Notes
    -----
    No data source is wired in yet. When one is added, its API key belongs here as a
    required ``pydantic.SecretStr`` field (no default), so that a missing key fails at
    start-up instead of halfway through a fetch.
    """

    model_config = SettingsConfigDict(
        env_prefix="GASSKEW_",
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_dir: Path = Path("data")
    checkpoint_dir: Path = Path("data/checkpoints")
    output_dir: Path = Path("outputs")
    db_name: str = "gasskew.sqlite"
    log_level: str = "INFO"

    @field_validator("data_dir", "checkpoint_dir", "output_dir")
    @classmethod
    def _resolve(cls, value: Path) -> Path:
        return value if value.is_absolute() else (PROJECT_ROOT / value).resolve()

    @field_validator("log_level")
    @classmethod
    def _check_level(cls, value: str) -> str:
        value = value.upper()
        if value not in LOG_LEVELS:
            raise ValueError(f"invalid log level {value!r}; expected one of {sorted(LOG_LEVELS)}")
        return value

    @property
    def db_path(self) -> Path:
        """Full path of the SQLite results database."""
        return self.output_dir / self.db_name


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings singleton.

    Returns
    -------
    Settings
        Validated settings.

    Raises
    ------
    pydantic.ValidationError
        If any environment value is malformed.
    """
    return Settings()
