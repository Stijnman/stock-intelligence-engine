"""Stock Intelligence Engine core package."""
from sie.analyzer import analyze_watchlist, run_report
from sie.social import scan_narrative_intelligence, integrate_social_to_row, forecast_narrative_phase
from sie.insider import detect_insider_cluster, integrate_insider_to_row
from sie.prediction_markets import detect_prediction_market_signal, integrate_prediction_markets_to_row
from sie.institutional import detect_institutional_change, integrate_institutional_to_row

__all__ = [
    "analyze_watchlist",
    "run_report",
    "scan_narrative_intelligence",
    "integrate_social_to_row",
    "forecast_narrative_phase",
    "detect_insider_cluster",
    "integrate_insider_to_row",
    "detect_prediction_market_signal",
    "integrate_prediction_markets_to_row",
    "detect_institutional_change",
    "integrate_institutional_to_row",
]

__version__ = "2.10.0"
