"""Orchestrate narrative + technical analysis."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sie.config import load_config
from sie.i18n import t, translate_reason
from sie.news import fetch_headlines
from sie.technical import analyze_ticker


def analyze_watchlist(
    cfg: dict[str, Any] | None = None,
    include_news: bool = False,
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
            row["headlines"] = [h.title for h in fetch_headlines(ticker, limit=2)]
        rows.append(row)

    return {
        "title": t(lang, "title"),
        "theme": theme,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "lang": lang,
        "rows": rows,
        "disclaimer": t(lang, "disclaimer"),
    }


def format_report(report: dict[str, Any]) -> str:
    lang = report.get("lang", "en")
    lines = [
        "",
        f"=== {report['title']} v2.0.0 ===",
        f"{t(lang, 'theme')}: {report['theme']}",
        f"{t(lang, 'updated')}: {report['timestamp']}",
        "",
    ]
    for row in report["rows"]:
        price = f"${row['price']}" if row.get("price") is not None else t(lang, "no_data")
        signal_label = t(lang, row.get("signal", "hold"))
        rsi = row.get("rsi", "—")
        dd = row.get("drawdown_pct", "—")
        lines.append(f"{row['color']} {row['ticker']} ({row['name']}): {price}")
        reason = translate_reason(row.get("signal_reason", ""), lang)
        lines.append(f"  {t(lang, 'signal')}: {signal_label} — {reason}")
        lines.append(f"  {t(lang, 'rsi')}: {rsi} | {t(lang, 'drawdown')}: {dd}%")
        lines.append(f"  {row.get('note', '')}")
        if row.get("headlines"):
            lines.append(f"  {t(lang, 'news')}:")
            for h in row["headlines"]:
                lines.append(f"    • {h}")
        if row.get("error"):
            lines.append(f"  ⚠ {row['error']}")
        lines.append("")

    lines.append(f"⚠️  {report['disclaimer']}")
    return "\n".join(lines)


def run_report(
    lang: str = "en",
    include_news: bool = False,
    export: bool = False,
    email: bool = False,
    export_dir: str = "exports",
) -> dict[str, Any]:
    cfg = load_config()
    report = analyze_watchlist(cfg, include_news=include_news, lang=lang)
    text = format_report(report)
    print(text)

    result: dict[str, Any] = {"report": report, "text": text}

    if export:
        from sie.export import export_csv

        flat_rows = []
        for row in report["rows"]:
            flat = {k: v for k, v in row.items() if k != "headlines"}
            if "headlines" in row:
                flat["headlines"] = " | ".join(row["headlines"])
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

    return result