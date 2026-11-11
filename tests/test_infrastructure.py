from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from gasskew.checkpoints import Stage, load_checkpoint, save_checkpoint
from gasskew.cli import app
from gasskew.config import Settings
from gasskew.exceptions import DataLoadError, DataValidationError
from gasskew.temporal import filter_as_of


def test_settings_resolve_relative_paths() -> None:
    s = Settings()
    assert s.data_dir.is_absolute()
    assert s.checkpoint_dir.is_absolute()
    assert s.db_path.parent == s.output_dir


def test_settings_read_prefixed_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GASSKEW_LOG_LEVEL", "debug")
    assert Settings().log_level == "DEBUG"


def test_settings_reject_bad_log_level() -> None:
    with pytest.raises(ValidationError):
        Settings(log_level="LOUD")


def test_filter_as_of_drops_future_rows() -> None:
    df = pd.DataFrame({"trade_date": pd.to_datetime(["2024-01-03", "2024-01-04", "2024-01-05"])})
    out = filter_as_of(df, date(2024, 1, 4))
    assert len(out) == 2
    assert out["trade_date"].max() == pd.Timestamp("2024-01-04")


def test_filter_as_of_on_index() -> None:
    df = pd.DataFrame({"x": [1, 2]}, index=pd.to_datetime(["2024-01-04", "2024-01-08"]))
    assert len(filter_as_of(df, date(2024, 1, 5))) == 1


def test_filter_as_of_rejects_string_dates() -> None:
    df = pd.DataFrame({"trade_date": ["2024-01-03", "2024-01-04"]})
    with pytest.raises(DataValidationError):
        filter_as_of(df, date(2024, 1, 4))


def test_checkpoint_roundtrip(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1.0, 2.0]})
    save_checkpoint(df, tmp_path, Stage.PARSED, "demo")
    pd.testing.assert_frame_equal(load_checkpoint(tmp_path, Stage.PARSED, "demo"), df)


def test_missing_checkpoint_raises(tmp_path: Path) -> None:
    with pytest.raises(DataLoadError):
        load_checkpoint(tmp_path, Stage.RAW, "nope")


def test_cli_info_runs() -> None:
    result = CliRunner().invoke(app, ["info"])
    assert result.exit_code == 0, result.output
    assert "data_dir" in result.output
