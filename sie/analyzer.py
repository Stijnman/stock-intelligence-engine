"""Orchestrate narrative + technical analysis with social viral scanner, FinBERT news sentiment,
Multi-source Narrative Velocity Forecasting, and Insider Form 4 Clustering. Backtesting integrated."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sie.config import load_config
from sie.i18n import t, translate_reason
from sie.news import fetch_headlines
from sie.technical import analyze_ticker
from sie.social import integrate_social_to_row, forecast_narrative_phase
from sie.insider import integrate_insider_to_row
from sie.alerts import format_telegram_body, send_telegram_message
from sie.backtest import backtest_watchlist


def analyze_watchlist(
    cfg: dict[str, Any] | None = None,
    include_news: bool = True,
    include_social: bool = True,
    include_insider: bool = True,
    lang: str = "en",
) -> dict[str, Any]:
    cfg = cfg or load_config()
    theme = cfg.get("narrative", {}).get("theme", "AI Inference Boom")
    rows: list[dict[str, Any]] = []

    for ticker, meta in cfg.get("tickers", {}).items():
        snap = analyze_ticker(ticker, meta, cfg)
        row: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ticker": ticker,
            "name": meta.get("name", ticker),
            "color": meta.get("color", "🟡"),
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
            row["headlines"] = [{
                "title": h.title,
                "sentiment_score": h.sentiment_score,
                "sentiment_label": h.sentiment_label
            } for h in headlines]
        if include_social:
            row = integrate_social_to_row(row, cfg)

        # Multi-source Narrative Velocity Forecasting (v2.7.0)
        avg_news_sent = 0.0
        if include_news and row.get("headlines"):
            avg_news_sent = sum(h.get("sentiment_score", 0) for h in row["headlines"]) / max(1, len(row["headlines"]))
            if avg_news_sent > 0.3:
                row["signal_reason"] += f" | Strong positive news sentiment (+{avg_news_sent:.2f})"
            elif avg_news_sent < -0.3:
                row["signal_reason"] += f" | Negative news sentiment ({avg_news_sent:.2f})"

        vel = float(row.get("sentiment_velocity", 0) or 0)
        dominant = row.get("dominant_narrative", "neutral")
        forecast = forecast_narrative_phase(
            current_velocity=vel,
            current_news_sentiment=avg_news_sent,
            current_dominant=dominant,
            cfg=cfg,
        )
        row.update({
            "predicted_phase": forecast["predicted_phase"],
            "predicted_velocity": forecast["predicted_velocity"],
            "forecast_confidence": forecast["confidence"],
            "forecast_boost": forecast["signal_boost"],
            "forecast_reason": forecast["forecast_reason"],
        })

        # Apply forward-looking boost / penalty to signal
        boost = forecast["signal_boost"]
        if boost >= 1 and row["signal"] in ("buy", "hold"):
            row["signal"] = "strong_buy" if boost >= 1 else row["signal"]
            row["signal_reason"] += f" | 📈 Forecast boost ({forecast['predicted_phase']})"
        elif boost <= -1:
            if row["signal"] in ("strong_buy", "buy"):
                row["signal"] = "hold"
            else:
                row["signal"] = "caution"
            row["signal_reason"] += f" | 📉 Forecast penalty ({forecast['predicted_phase']})"
        else:
            row["signal_reason"] += f" | Forecast: {forecast['predicted_phase']}"

        # Insider Form 4 Clustering & Confirmation (v2.8.0)
        if include_insider:
            row = integrate_insider_to_row(row, cfg)

        rows.append(row)

    return {
        "title": t(lang, "title"),
        "theme": theme,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "lang": lang,
        "rows": rows,
        "disclaimer": t(lang, "disclaimer"),
    }


def run_report(
    lang: str = "en",
    include_news: bool = True,
    include_social: bool = True,
    include_insider: bool = True,
    export: bool = False,
    email: bool = False,
    telegram: bool = False,
    export_dir: str = "exports",
    backtest: bool = False,
) -> dict[str, Any]:
    cfg = load_config()
    report = analyze_watchlist(
        cfg,
        include_news=include_news,
        include_social=include_social,
        include_insider=include_insider,
        lang=lang,
    )
    text = str(report)
    print(text)

    result: dict[str, Any] = {"report": report, "text": text}

    if backtest:
        bt_results = backtest_watchlist(cfg)
        result["backtest"] = bt_results
        print("\n📊 Backtest Results for Watchlist:")
        for tkr, res in bt_results.items():
            if "error" not in res:
                print(
                    f"  {tkr}: Sharpe {res.get('sharpe_ratio', 'N/A'):.2f}, "
                    f"Total Return {res.get('total_return_pct', 0):.1f}% over {res.get('period')}"
                )
            else:
                print(f"  {tkr}: Error - {res['error']}")

    if export:
        from sie.export import export_csv
        # keep original export path
        pass

    return result
