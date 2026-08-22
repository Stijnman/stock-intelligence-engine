"""Stock Intelligence Engine package public API."""

from .alerts import send_email_report, send_telegram_message
from .analyzer import analyze_watchlist, run_report
from .backtest import backtest_watchlist, run_backtest
from .config import load_config
from .congressional import detect_congressional_trades, integrate_congressional_to_row
from .dark_pool import detect_dark_pool_flow, integrate_dark_pool_to_row
from .export import export_csv
from .hiring import detect_hiring_momentum, integrate_hiring_to_row
from .i18n import t
from .insider import detect_insider_cluster, integrate_insider_to_row
from .institutional import detect_institutional_change, integrate_institutional_to_row
from .news import fetch_headlines
from .options_0dte import detect_options_0dte, integrate_options_0dte_to_row
from .options_iv import detect_options_iv, integrate_options_iv_to_row
from .portfolio import (
    compute_portfolio_overlay,
    correlation_heatmap_figure,
    correlation_matrix,
    portfolio_risk_metrics,
)
from .prediction_markets import (
    detect_prediction_market_signal,
    integrate_prediction_markets_to_row,
)
from .realtime import get_realtime_quote, integrate_realtime_to_row
from .social import scan_narrative_intelligence
from .technical import TechnicalSnapshot, analyze_ticker, compute_signal
from .thesis import generate_thesis_pair, integrate_thesis_to_row

__all__ = [
    "TechnicalSnapshot",
    "analyze_ticker",
    "analyze_watchlist",
    "backtest_watchlist",
    "compute_portfolio_overlay",
    "compute_signal",
    "correlation_heatmap_figure",
    "correlation_matrix",
    "detect_congressional_trades",
    "detect_dark_pool_flow",
    "detect_hiring_momentum",
    "detect_insider_cluster",
    "detect_institutional_change",
    "detect_options_0dte",
    "detect_options_iv",
    "detect_prediction_market_signal",
    "export_csv",
    "fetch_headlines",
    "generate_thesis_pair",
    "get_realtime_quote",
    "integrate_congressional_to_row",
    "integrate_dark_pool_to_row",
    "integrate_hiring_to_row",
    "integrate_insider_to_row",
    "integrate_institutional_to_row",
    "integrate_options_0dte_to_row",
    "integrate_options_iv_to_row",
    "integrate_prediction_markets_to_row",
    "integrate_realtime_to_row",
    "integrate_thesis_to_row",
    "load_config",
    "portfolio_risk_metrics",
    "run_backtest",
    "run_report",
    "scan_narrative_intelligence",
    "send_email_report",
    "send_telegram_message",
    "t",
]

__version__ = "2.20.2"
