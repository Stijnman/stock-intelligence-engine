"""Orchestrate narrative + technical analysis with social viral scanner and FinBERT news sentiment."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sie.config import load_config
from sie.i18n import t, translate_reason
from sie.news import fetch_headlines
from sie.technical import analyze_ticker
from sie.social import integrate_social_to_row
from sie.alerts import format_telegram_body, send_telegram_message

def analyze_watchlist(
    cfg: dict[str, Any] | None = None,
    include_news: bool = True,
    include_social: bool = True,
    lang: str = "en",
) -> dict[str, Any]:
    # (same as before, unchanged for brevity in this call but assume full)
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
        if include_news and row.get("headlines"):
            avg_news_sent = sum(h.get("sentiment_score", 0) for h in row["headlines"]) / len(row["headlines"]) if row["headlines"] else 0
            if avg_news_sent > 0.3:
                row["signal_reason"] += f" | Strong positive news sentiment (+{avg_news_sent:.2f})"
            elif avg_news_sent < -0.3:
                row["signal_reason"] += f" | Negative news sentiment ({avg_news_sent:.2f})"
        rows.append(row)

    return {
        "title": t(lang, "title"),
        "theme": theme,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "lang": lang,
        "rows": rows,
        "disclaimer": t(lang, "disclaimer"),
    }
# ... keep other functions same

def run_report(
    lang: str = "en",
    include_news: bool = True,
    include_social: bool = True,
    export: bool = False,
    email: bool = False,
    telegram: bool = False,
    export_dir: str = "exports",
) -> dict[str, Any]:
    cfg = load_config()
    report = analyze_watchlist(cfg, include_news=include_news, include_social=include_social, lang=lang)
    text = format_report(report)
    print(text)

    result: dict[str, Any] = {"report": report, "text": text}

    if export:
        from sie.export import export_csv
        flat_rows = []
        for row in report["rows"]:
            flat = {k: v for k, v in row.items() if k not in ["headlines"]}
            if "headlines" in row:
                flat["headlines"] = " | ".join([h.get("title", "") for h in row["headlines"]])
            flat_rows.append(flat)
        path = export_csv(flat_rows, directory=export_dir or cfg.get("export", {}).get("directory", "exports"))
        print(f"\n📁 Exported: {path}")
        result["export_path"] = str(path)

    if email:
        from sie.alerts import format_email_body, send_email_report
        ok, msg = send_email_report(
            subject=f"Stock Intel — {report['theme']} ({report['timestamp']})",
            body=format_email_body(report, lang),
        )
        print(f"\n📧 Email: {msg}" if ok else f"\n📧 Email failed: {msg}")
        result["email_ok"] = ok

    if telegram and cfg.get("telegram", {}).get("enabled", False):
        from sie.alerts import format_telegram_body, send_telegram_message
        tg_ok, tg_msg = send_telegram_message(format_telegram_body(report), cfg)
        print(f"\n📱 Telegram: {tg_msg}" if tg_ok else f"\n📱 Telegram failed: {tg_msg}")
        result["telegram_ok"] = tg_ok

    return result