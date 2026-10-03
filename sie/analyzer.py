"""Orchestrate narrative + technical analysis including ETF AP flow, 10b5-1 buybacks and Dealer GEX."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from sie.config import load_config
from sie.i18n import t
from sie.news import fetch_headlines
from sie.technical import analyze_ticker
from sie.social import integrate_social_to_row, forecast_narrative_phase
from sie.insider import integrate_insider_to_row
from sie.prediction_markets import integrate_prediction_markets_to_row
from sie.institutional import integrate_institutional_to_row
from sie.congressional import integrate_congressional_to_row
from sie.realtime import integrate_realtime_to_row
from sie.dark_pool import integrate_dark_pool_to_row
from sie.options_iv import integrate_options_iv_to_row
from sie.options_0dte import integrate_options_0dte_to_row
from sie.edgar import integrate_edgar_to_row
from sie.hiring import integrate_hiring_to_row
from sie.hiring_skill_mix import integrate_hiring_skill_mix_to_row
from sie.supply_chain import integrate_supply_chain_to_row
from sie.short_interest import integrate_short_interest_to_row
from sie.attention import integrate_attention_to_row
from sie.authenticity import integrate_authenticity_to_row
from sie.social_intent import integrate_social_intent_to_row
from sie.credit_spread import integrate_credit_spread_to_row
from sie.earnings_call import integrate_earnings_call_to_row
from sie.news_authority import integrate_news_authority_to_row
from sie.whisper_number import integrate_whisper_number_to_row
from sie.kol_amplification import integrate_kol_amplification_to_row
from sie.etf_flow import integrate_etf_flow_to_row
from sie.buyback_10b51 import integrate_buyback_10b51_to_row
from sie.employee_outlook import integrate_employee_outlook_to_row
from sie.app_store_reviews import integrate_app_store_reviews_to_row
from sie.retail_flow import integrate_retail_flow_to_row
from sie.unusual_options import integrate_unusual_options_to_row
from sie.consumer_spend import integrate_consumer_spend_to_row
from sie.borrow_fee import integrate_borrow_fee_to_row
from sie.contagion import integrate_contagion_to_row
from sie.estimate_revision import integrate_estimate_revision_to_row
from sie.patent_momentum import integrate_patent_momentum_to_row
from sie.digital_footprint import integrate_digital_footprint_to_row
from sie.gex import integrate_gex_to_row
from sie.tokenized_basis import integrate_tokenized_basis_to_row
from sie.news_materiality import integrate_news_materiality_to_row
from sie.dilution_atm import integrate_dilution_atm_to_row
from sie.trace_flow import integrate_trace_flow_to_row
from sie.thesis import integrate_thesis_to_row
from sie.brief import integrate_brief_to_row
from sie.honesty import integrate_honesty_to_row
from sie.confidence import integrate_confidence_to_row
from sie.regime import integrate_regime_to_row
from sie.backtest import backtest_watchlist

OVERLAYS: list[tuple[str, Callable]] = [
    ("include_insider", integrate_insider_to_row),
    ("include_pm", integrate_prediction_markets_to_row),
    ("include_institutional", integrate_institutional_to_row),
    ("include_congressional", integrate_congressional_to_row),
    ("include_realtime", integrate_realtime_to_row),
    ("include_dark_pool", integrate_dark_pool_to_row),
    ("include_options_iv", integrate_options_iv_to_row),
    ("include_options_0dte", integrate_options_0dte_to_row),
    ("include_edgar", integrate_edgar_to_row),
    ("include_hiring", integrate_hiring_to_row),
    ("include_supply_chain", integrate_supply_chain_to_row),
    ("include_short_interest", integrate_short_interest_to_row),
    ("include_attention", integrate_attention_to_row),
    ("include_authenticity", integrate_authenticity_to_row),
    ("include_social_intent", integrate_social_intent_to_row),
    ("include_credit_spread", integrate_credit_spread_to_row),
    ("include_earnings_call", integrate_earnings_call_to_row),
    ("include_news_authority", integrate_news_authority_to_row),
    ("include_whisper_number", integrate_whisper_number_to_row),
    ("include_kol_amplification", integrate_kol_amplification_to_row),
    ("include_etf_flow", integrate_etf_flow_to_row),
    ("include_buyback_10b51", integrate_buyback_10b51_to_row),
    ("include_employee_outlook", integrate_employee_outlook_to_row),
    ("include_app_store_reviews", integrate_app_store_reviews_to_row),
    ("include_retail_flow", integrate_retail_flow_to_row),
    ("include_unusual_options", integrate_unusual_options_to_row),
    ("include_consumer_spend", integrate_consumer_spend_to_row),
    ("include_borrow_fee", integrate_borrow_fee_to_row),
    ("include_contagion", integrate_contagion_to_row),
    ("include_estimate_revision", integrate_estimate_revision_to_row),
    ("include_patent_momentum", integrate_patent_momentum_to_row),
    ("include_digital_footprint", integrate_digital_footprint_to_row),
    ("include_gex", integrate_gex_to_row),
    ("include_hiring_skill_mix", integrate_hiring_skill_mix_to_row),
    ("include_tokenized_basis", integrate_tokenized_basis_to_row),
    ("include_news_materiality", integrate_news_materiality_to_row),
    ("include_dilution_atm", integrate_dilution_atm_to_row),
    ("include_trace_flow", integrate_trace_flow_to_row),
    ("include_thesis", integrate_thesis_to_row),
    ("include_brief", integrate_brief_to_row),
    ("include_honesty", integrate_honesty_to_row),
    ("include_confidence", integrate_confidence_to_row),
    ("include_regime", integrate_regime_to_row),
]


def analyze_watchlist(cfg: dict[str, Any] | None = None, include_news: bool = True, include_social: bool = True, lang: str = "en", **flags: Any) -> dict[str, Any]:
    cfg = cfg or load_config()
    theme = cfg.get("narrative", {}).get("theme", "AI Inference Boom")
    rows: list[dict[str, Any]] = []
    for ticker, meta in cfg.get("tickers", {}).items():
        snap = analyze_ticker(ticker, meta, cfg)
        row: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ticker": ticker,
            "name": meta.get("name", ticker),
            "color": meta.get("color", "\ud83d\udfe1"),
            "note": meta.get("note", ""),
            "narrative_fit": meta.get("narrative_fit", "monitor"),
            "theme": theme,
            "price": round(snap.price, 2) if snap.price is not None else None,
            "ma50": round(snap.ma_fast, 2) if snap.ma_fast is not None else None,
            "ma200": round(snap.ma_slow, 2) if snap.ma_slow is not None else None,
            "rsi": round(snap.rsi, 1) if snap.rsi is not None else None,
            "high_52w": round(snap.high_52w, 2) if snap.high_52w is not None else None,
            "drawdown_pct": round(snap.drawdown_pct, 1) if snap.drawdown_pct is not None else None,
            "signal": snap.signal,
            "signal_reason": snap.signal_reason,
            "error": snap.error,
        }
        if include_news:
            headlines = fetch_headlines(ticker, limit=2)
            row["headlines"] = [{"title": h.title, "sentiment_score": h.sentiment_score, "sentiment_label": h.sentiment_label} for h in headlines]
        if include_social:
            row = integrate_social_to_row(row, cfg)
        avg_news_sent = 0.0
        if include_news and row.get("headlines"):
            avg_news_sent = sum(h.get("sentiment_score", 0) for h in row["headlines"]) / max(1, len(row["headlines"]))
            if avg_news_sent > 0.3:
                row["signal_reason"] += f" | Strong positive news sentiment (+{avg_news_sent:.2f})"
            elif avg_news_sent < -0.3:
                row["signal_reason"] += f" | Negative news sentiment ({avg_news_sent:.2f})"
        vel = float(row.get("sentiment_velocity", 0) or 0)
        dominant = row.get("dominant_narrative", "neutral")
        forecast = forecast_narrative_phase(current_velocity=vel, current_news_sentiment=avg_news_sent, current_dominant=dominant, cfg=cfg)
        row.update({"predicted_phase": forecast["predicted_phase"], "predicted_velocity": forecast["predicted_velocity"], "forecast_confidence": forecast["confidence"], "forecast_boost": forecast["signal_boost"], "forecast_reason": forecast["forecast_reason"]})
        boost = forecast["signal_boost"]
        if boost >= 1 and row["signal"] in ("buy", "hold"):
            row["signal"] = "strong_buy"
            row["signal_reason"] += f" | Forecast boost ({forecast['predicted_phase']})"
        elif boost <= -1:
            row["signal"] = "hold" if row["signal"] in ("strong_buy", "buy") else "caution"
            row["signal_reason"] += f" | Forecast penalty ({forecast['predicted_phase']})"
        else:
            row["signal_reason"] += f" | Forecast: {forecast['predicted_phase']}"
        for flag_name, fn in OVERLAYS:
            if flags.get(flag_name, True):
                row = fn(row, cfg)
        rows.append(row)
    return {"title": t(lang, "title"), "theme": theme, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "lang": lang, "rows": rows, "disclaimer": t(lang, "disclaimer")}


def run_report(lang: str = "en", include_news: bool = True, include_social: bool = True, export: bool = False, email: bool = False, telegram: bool = False, export_dir: str = "exports", backtest: bool = False, **flags: Any) -> dict[str, Any]:
    cfg = load_config()
    report = analyze_watchlist(cfg, include_news=include_news, include_social=include_social, lang=lang, **flags)
    text = str(report)
    print(text)
    result: dict[str, Any] = {"report": report, "text": text}
    if backtest:
        bt_results = backtest_watchlist(cfg)
        result["backtest"] = bt_results
        print("\\nBacktest Results for Watchlist:")
        for tkr, res in bt_results.items():
            if "error" not in res:
                print(f"  {tkr}: Sharpe {res.get('sharpe_ratio', 'N/A'):.2f}, Total Return {res.get('total_return_pct', 0):.1f}% over {res.get('period')}")
            else:
                print(f"  {tkr}: Error - {res['error']}")
    if export:
        from sie.export import export_csv
        export_path = export_csv(report.get("rows", []), directory=export_dir)
        result["export_path"] = str(export_path)
        print(f"Exported report to {export_path}")
    return result
