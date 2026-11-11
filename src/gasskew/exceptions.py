"""Domain-specific exceptions.

Every expected failure state in the pipeline raises one of these, so callers never
need to catch the broad ``Exception`` base class.
"""

from __future__ import annotations


class GasSkewError(Exception):
    """Base class for all gasskew errors."""


class ConfigError(GasSkewError):
    """Configuration is missing or invalid (e.g. a bad path or API key in ``.env``)."""


class DataFetchError(GasSkewError):
    """A request to a remote data source failed or returned an unusable payload."""


class DataLoadError(GasSkewError):
    """A local input file or checkpoint is missing or cannot be parsed."""


class DataValidationError(GasSkewError):
    """Loaded data violates a schema or a market-data invariant."""


class StaleDataError(GasSkewError):
    """No market data is available on or close enough before the requested ``as_of``."""


class LookAheadError(GasSkewError):
    """Data dated after ``as_of`` reached a pricing, calibration or analysis function."""


class CalibrationError(GasSkewError):
    """Implied-vol inversion or smile fitting failed."""


class PricingError(GasSkewError):
    """A pricer failed to produce a valid price (e.g. root-finding did not converge)."""
