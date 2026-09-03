"""Webhook / Multi-Channel Alert Router with Overlay Threshold Triggers.

Extends the alert system to support configurable Discord, Telegram and
generic webhook payloads. Alerts fire when configurable overlay combinations
are met (e.g. high confidence + squeeze risk + rising narrative velocity).

Features:
- Discord webhook (simple JSON content / embeds)
- Telegram bot (Bot API sendMessage)
- Generic webhooks (JSON POST with templated body)
- Rate-limiting (per-channel cooldown seconds)
- Deduplication (ticker + signal key hash, short TTL)
- Threshold triggers driven from config.yaml `alerts.triggers`
- Backward-compatible format_telegram_body / send_telegram_message

No invented secrets. User must supply bot tokens / webhook URLs via
config.yaml or environment variables. Live delivery is best-effort and
never blocks the main analysis pipeline.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from sie.config import load_config

_STATE_FILE = Path(os.environ.get("SIE_ALERT_STATE", "/tmp/sie_alert_state.json"))
_DEFAULT_COOLDOWN = 300
_DEFAULT_DEDUPE_TTL = 900

def _load_state() -> dict:
    try:
        if _STATE_FILE.exists():
            return json.loads(_STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"last_sent": {}, "dedupe": {}}

def _save_state(state: dict) -> None:
    try:
        _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _STATE_FILE.write_text(json.dumps(state, indent=0), encoding="utf-8")
    except Exception:
        pass

def _now_ts() -> float:
    return time.time()

def _channel_allowed(channel: str, cooldown: int, state: dict) -> bool:
    last = float(state.get("last_sent", {}).get(channel, 0))
    return (_now_ts() - last) >= cooldown

def _mark_sent(channel: str, state: dict) -> None:
    state.setdefault("last_sent", {})[channel] = _now_ts()

def _dedupe_key(ticker: str, signal: str, reason_snippet: str) -> str:
    raw = f"{ticker}|{signal}|{reason_snippet[:80]}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def _is_duplicate(key: str, ttl: int, state: dict) -> bool:
    entry = state.get("dedupe", {}).get(key)
    if not entry:
        return False
    return (_now_ts() - float(entry)) < ttl

def _mark_dedupe(key: str, state: dict) -> None:
    state.setdefault("dedupe", {})[key] = _now_ts()
    cutoff = _now_ts() - 3600
    state["dedupe"] = {k: v for k, v in state["dedupe"].items() if float(v) > cutoff}

def format_telegram_body(report: dict | None = None, rows: list | None = None) -> str:
    rows = rows or (report or {}).get("rows") or []
    theme = (report or {}).get("theme", "watchlist")
    ts = (report or {}).get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    lines = [f"📡 *Stock Intelligence Engine* — {theme}", f"_{ts}_", ""]
    for r in rows[:12]:
        tkr = r.get("ticker", "?")
        sig = r.get("signal", "n/a")
        conf = r.get("confidence_score", r.get("conf_score", 0))
        try:
            conf_f = float(conf)
        except Exception:
            conf_f = 0.0
        reason = (r.get("signal_reason") or r.get("bf_reason") or "")[:90]
        lines.append(f"*{tkr}* `{sig}` conf={conf_f:.2f} — {reason}")
    lines.append("")
    lines.append("_Not financial advice. See DISCLAIMER.md_")
    return "\n".join(lines)

def send_telegram_message(text: str, cfg: dict | None = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    tg = cfg.get("telegram") or {}
    token = (tg.get("bot_token") or os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat_id = (tg.get("chat_id") or os.environ.get("TELEGRAM_CHAT_ID") or "").strip()
    if not token or not chat_id or not tg.get("enabled", False):
        return {"ok": False, "error": "telegram disabled or missing token/chat_id"}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        resp = requests.post(url, json=payload, timeout=12)
        data = resp.json() if "application/json" in (resp.headers.get("content-type") or "") else {}
        return {"ok": resp.status_code < 400 and data.get("ok", False), "status": resp.status_code, "data": data}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

def _send_discord(webhook_url: str, content: str, embeds: list | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"content": content[:2000]}
    if embeds:
        payload["embeds"] = embeds[:10]
    try:
        resp = requests.post(webhook_url, json=payload, timeout=12)
        return {"ok": resp.status_code in (200, 204), "status": resp.status_code}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

def _send_generic_webhook(url: str, body: dict) -> dict[str, Any]:
    try:
        resp = requests.post(url, json=body, timeout=12, headers={"Content-Type": "application/json"})
        return {"ok": resp.status_code < 400, "status": resp.status_code}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

def _row_matches_trigger(row: dict, trigger: dict) -> bool:
    signals = trigger.get("signals")
    if signals:
        if str(row.get("signal", "")).lower() not in {s.lower() for s in signals}:
            return False
    min_conf = trigger.get("min_confidence")
    if min_conf is not None:
        conf = float(row.get("confidence_score") or row.get("conf_score") or row.get("confidence") or 0)
        if conf < float(min_conf):
            return False
    min_vel = trigger.get("min_narrative_velocity")
    if min_vel is not None:
        vel = float(row.get("predicted_velocity") or row.get("sentiment_velocity") or 0)
        if vel < float(min_vel):
            return False
    if trigger.get("require_squeeze_boost"):
        if int(row.get("bf_boost") or 0) < 1:
            return False
    require_boosts = trigger.get("require_any_boost") or []
    if require_boosts:
        found = False
        for key in require_boosts:
            if int(row.get(key) or 0) >= 1:
                found = True
                break
        if not found:
            return False
    min_auth = trigger.get("min_authenticity")
    if min_auth is not None:
        auth = float(row.get("auth_score") or row.get("authenticity_score") or 1.0)
        if auth < float(min_auth):
            return False
    return True

def evaluate_triggers(rows: list[dict], cfg: dict | None = None) -> list[dict]:
    cfg = cfg or load_config()
    alerts_cfg = cfg.get("alerts") or {}
    triggers = alerts_cfg.get("triggers") or []
    if not triggers:
        triggers = [{"name": "high_conviction_combo", "signals": ["strong_buy", "buy"], "min_confidence": 0.60, "min_narrative_velocity": 1.0, "require_any_boost": ["bf_boost", "auth_boost", "supply_boost", "cs_boost"]}]
    matched = []
    for row in rows:
        for tr in triggers:
            if _row_matches_trigger(row, tr):
                matched.append({"ticker": row.get("ticker"), "signal": row.get("signal"), "reason": (row.get("signal_reason") or "")[:200], "trigger_name": tr.get("name", "unnamed"), "confidence": row.get("confidence_score") or row.get("conf_score"), "row": row})
                break
    return matched

def build_alert_payload(matched: list[dict], report: dict | None = None) -> dict:
    theme = (report or {}).get("theme", "watchlist")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"🚨 SIE Alert — {theme} @ {ts}"]
    for m in matched[:8]:
        lines.append(f"• {m['ticker']} `{m['signal']}` conf={m.get('confidence')} [{m['trigger_name']}] — {m['reason'][:100]}")
    text = "\n".join(lines)
    embeds = []
    for m in matched[:5]:
        color = 0x00C853 if "buy" in str(m["signal"]).lower() else 0xFF6D00
        embeds.append({"title": f"{m['ticker']} — {m['signal']}", "description": m["reason"][:300], "color": color, "fields": [{"name": "Trigger", "value": str(m["trigger_name"]), "inline": True}, {"name": "Confidence", "value": str(m.get("confidence")), "inline": True}]})
    return {"text": text, "embeds": embeds, "matched_count": len(matched), "timestamp": ts, "theme": theme}

def route_alerts(report: dict | None = None, rows: list | None = None, cfg: dict | None = None, force: bool = False) -> dict[str, Any]:
    cfg = cfg or load_config()
    alerts_cfg = cfg.get("alerts") or {}
    if not alerts_cfg.get("enabled", True) and not force:
        return {"ok": False, "skipped": True, "reason": "alerts.enabled is false"}
    rows = rows or (report or {}).get("rows") or []
    if not rows:
        return {"ok": False, "skipped": True, "reason": "no rows"}
    matched = evaluate_triggers(rows, cfg)
    if not matched and not force:
        return {"ok": True, "matched": 0, "sent": {}, "reason": "no triggers matched"}
    payload = build_alert_payload(matched, report)
    state = _load_state()
    cooldown = int(alerts_cfg.get("cooldown_seconds", _DEFAULT_COOLDOWN))
    dedupe_ttl = int(alerts_cfg.get("dedupe_ttl_seconds", _DEFAULT_DEDUPE_TTL))
    results: dict[str, Any] = {"matched": len(matched), "sent": {}, "payload_preview": payload["text"][:300]}
    if matched:
        dk = _dedupe_key(str(matched[0]["ticker"]), str(matched[0]["signal"]), matched[0]["reason"])
        if _is_duplicate(dk, dedupe_ttl, state) and not force:
            return {"ok": True, "matched": len(matched), "skipped": True, "reason": "deduplicated"}
        _mark_dedupe(dk, state)
    tg_cfg = cfg.get("telegram") or {}
    if (alerts_cfg.get("telegram") or tg_cfg.get("enabled")) and _channel_allowed("telegram", cooldown, state):
        body = format_telegram_body(report, rows) if not matched else payload["text"]
        tg_res = send_telegram_message(body.replace("*", "").replace("`", ""), cfg)
        results["sent"]["telegram"] = tg_res
        if tg_res.get("ok"):
            _mark_sent("telegram", state)
    discord_url = (alerts_cfg.get("discord_webhook") or os.environ.get("DISCORD_WEBHOOK_URL") or "").strip()
    if discord_url and _channel_allowed("discord", cooldown, state):
        d_res = _send_discord(discord_url, payload["text"], payload.get("embeds"))
        results["sent"]["discord"] = d_res
        if d_res.get("ok"):
            _mark_sent("discord", state)
    webhooks = alerts_cfg.get("webhooks") or []
    if isinstance(webhooks, str):
        webhooks = [webhooks]
    for i, url in enumerate(webhooks):
        url = (url or "").strip()
        if not url:
            continue
        ch = f"webhook_{i}"
        if not _channel_allowed(ch, cooldown, state):
            continue
        body = {"source": "stock-intelligence-engine", "version": "2.30.0", "timestamp": payload["timestamp"], "theme": payload["theme"], "matched": [{k: v for k, v in m.items() if k != "row"} for m in matched], "text": payload["text"]}
        w_res = _send_generic_webhook(url, body)
        results["sent"][ch] = w_res
        if w_res.get("ok"):
            _mark_sent(ch, state)
    _save_state(state)
    results["ok"] = True
    return results

def maybe_send_alerts(report: dict, cfg: dict | None = None, force: bool = False) -> dict[str, Any]:
    return route_alerts(report=report, cfg=cfg, force=force)
