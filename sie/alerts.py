"""Email + Telegram alerts for stock intelligence engine."""

from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from typing import Any

import requests
from dotenv import load_dotenv


def send_telegram_message(message: str, cfg: dict[str, Any] | None = None) -> tuple[bool, str]:
    """Send alert to Telegram channel."""
    if cfg is None:
        cfg = {}
    load_dotenv()
    token = cfg.get("telegram", {}).get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = cfg.get("telegram", {}).get("chat_id") or os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return False, "Telegram not configured — add to config.yaml or .env"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        return True, f"Sent to Telegram chat {chat_id}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def send_email_report(subject: str, body: str) -> tuple[bool, str]:
    load_dotenv()
    host = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    from_addr = os.getenv("FROM_EMAIL", user)
    to_addr = os.getenv("TO_EMAIL", user)

    if not all([user, password, to_addr]):
        return False, "Email not configured — copy .env.example to .env"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    try:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
        return True, f"Sent to {to_addr}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def format_email_body(report: dict[str, Any], lang: str = "en") -> str:
    lines = [
        report.get("title", "Stock Intelligence Engine"),
        f"Theme: {report['theme']}",
        f"Updated: {report['timestamp']}",
        "",
    ]
    for row in report.get("rows", []):
        lines.append(
            f"{row['color']} {row['ticker']} ({row['name']}): "
            f"${row.get('price', 'N/A')} | Signal: {row['signal']} | RSI: {row.get('rsi', 'N/A')}"
        )
        lines.append(f"  {row.get('note', '')}")
        lines.append(f"  {row.get('signal_reason', '')}")
        lines.append("")
    lines.append(report.get("disclaimer", ""))
    return "\n".join(lines)

def format_telegram_body(report: dict[str, Any]) -> str:
    """HTML formatted for Telegram."""
    lines = [
        f"<b>Stock Intelligence Engine</b> - {report.get('theme', '')}",
        f"Updated: {report.get('timestamp', '')}",
        "",
    ]
    for row in report.get("rows", []):
        signal = row.get('signal', 'hold').upper()
        lines.append(f"{row.get('color', '')} <b>{row['ticker']}</b>: {signal} | ${row.get('price', 'N/A')}")
        lines.append(f"RSI: {row.get('rsi', '—')} | DD: {row.get('drawdown_pct', '—')}%")
        if 'buzz_score' in row:
            lines.append(f"Buzz: {row.get('buzz_score', 0)}")
        lines.append(f"Note: {row.get('note', '')}")
        lines.append("---")
    return "\n".join(lines)
