"""Stock Intelligence Engine package."""

from .analyzer import analyze_watchlist, run_report
from .config import load_config
from .technical import compute_rsi, compute_ma
from .social import scan_narratives
from .news import fetch_headlines
from .insider import compute_insider_overlay
from .institutional import compute_institutional_overlay
from .prediction_markets import compute_pm_overlay
from .congressional import compute_congressional_overlay
from .portfolio import compute_portfolio_overlay
from .realtime import get_realtime_quotes
from .dark_pool import compute_dark_pool_overlay
from .options_iv import detect_options_iv, integrate_options_iv_to_row
from .backtest import run_backtest
from .alerts import send_alerts
from .export import export_report
from .charts import plot_correlation_heatmap
from .i18n import t

__all__ = [
    "analyze_watchlist",
    "run_report",
    "load_config",
    "compute_rsi",
    "compute_ma",
    "scan_narratives",
    "fetch_headlines",
    "compute_insider_overlay",
    "compute_institutional_overlay",
    "compute_pm_overlay",
    "compute_congressional_overlay",
    "compute_portfolio_overlay",
    "get_realtime_quotes",
    "compute_dark_pool_overlay",
    "detect_options_iv",
    "integrate_options_iv_to_row",
    "run_backtest",
    "send_alerts",
    "export_report",
    "plot_correlation_heatmap",
    "t",
    "correlation_matrix",
    "portfolio_risk_metrics",
]

__version__ = "2.15.0"
