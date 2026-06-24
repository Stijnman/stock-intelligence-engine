"""Optional SMTP email alerts."""

from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from typing import Any

from dotenv import load_dotenv


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