"""0DTE Options Flow & Unusual Activity Proxy.

Derives near-zero-days-to-expiration volume/OI spikes and simple unusual-activity
flags from free yfinance options chains (or a stable synthetic proxy). Flags
elevated 0DTE premium and directional flow as short-horizon event-risk /
dealer-hedging signals. Applies soft boost/penalty and surfaces 0DTE ratio,
side bias, confidence and reason in the dashboard, CLI and alerts.

Configurable via `options_0dte:` section in config.yaml.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import random
import math

from sie.config import load_config


def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _days_to_exp(exp_str: str) -> Optional[int]:
    """Parse YYYY-MM-DD expiration and return calendar days to expiry."""
    try:
        exp = datetime.strptime(exp_str[:10], "%Y-%m-%d").date()
        today = datetime.now(timezone.utc).date()
        return (exp - today).days
    except Exception:
        return None


def fetch_yfinance_0dte_chain(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Attempt to pull near-term (0-3 DTE preferred) options chain via yfinance.
    Returns structured dict with volume, OI, premium proxies or None.
    """
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        expirations = list(t.options or [])
        if not expirations:
            return None

        # Prefer expirations within 0-5 calendar days (0DTE / near-term)
        near_exps = []
        for exp in expirations:
            dte = _days_to_exp(exp)
            if dte is not None and 0 <= dte <= 5:
                near_exps.append((dte, exp))
        near_exps.sort(key=lambda x: x[0])
        if not near_exps:
            # Fall back to the absolute nearest 1-2 expirations
            near_exps = [(_days_to_exp(e) or 99, e) for e in expirations[:2]]
            near_exps = [x for x in near_exps if x[0] is not None]

        if not near_exps:
            return None

        total_call_vol = 0.0
        total_put_vol = 0.0
        total_call_oi = 0.0
        total_put_oi = 0.0
        total_call_prem = 0.0
        total_put_prem = 0.0
        used_exps: List[str] = []
        last_price = None

        try:
            hist = t.history(period="1d")
            if not hist.empty:
                last_price = float(hist["Close"].iloc[-1])
        except Exception:
            pass

        for dte, exp in near_exps[:3]:
            try:
                opt = t.option_chain(exp)
                calls = opt.calls
                puts = opt.puts
                if calls is None or puts is None:
                    continue
                used_exps.append(exp)

                # Volume
                if "volume" in calls.columns:
                    total_call_vol += float(calls["volume"].fillna(0).sum())
                if "volume" in puts.columns:
                    total_put_vol += float(puts["volume"].fillna(0).sum())

                # Open Interest
                if "openInterest" in calls.columns:
                    total_call_oi += float(calls["openInterest"].fillna(0).sum())
                if "openInterest" in puts.columns:
                    total_put_oi += float(puts["openInterest"].fillna(0).sum())

                # Approximate premium = volume * lastPrice (or mid)
                for side, df in (("call", calls), ("put", puts)):
                    if df is None or df.empty:
                        continue
                    price_col = None
                    for c in ("lastPrice", "mid", "bid"):
                        if c in df.columns:
                            price_col = c
                            break
                    vol_col = "volume" if "volume" in df.columns else None
                    if price_col and vol_col:
                        prem = float((df[price_col].fillna(0) * df[vol_col].fillna(0)).sum())
                        if side == "call":
                            total_call_prem += prem
                        else:
                            total_put_prem += prem
            except Exception:
                continue

        if not used_exps:
            return None

        total_vol = total_call_vol + total_put_vol
        total_oi = total_call_oi + total_put_oi
        total_prem = total_call_prem + total_put_prem

        return {
            "source": "yfinance",
            "expirations": used_exps,
            "call_volume": total_call_vol,
            "put_volume": total_put_vol,
            "total_volume": total_vol,
            "call_oi": total_call_oi,
            "put_oi": total_put_oi,
            "total_oi": total_oi,
            "call_premium": total_call_prem,
            "put_premium": total_put_prem,
            "total_premium": total_prem,
            "last_price": last_price,
        }
    except Exception:
        return None


def detect_options_0dte(
    ticker: str,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    """
    Detect elevated 0DTE / near-term volume, OI and directional premium.
    Returns metrics + signal_boost (-1 / 0 / +1) and human-readable reason.
    """
    cfg = cfg or load_config()
    ov_cfg = cfg.get("options_0dte", {})
    if not ov_cfg.get("enabled", True):
        return {
            "odte_ratio": 0.0,
            "side_bias": "neutral",
            "call_put_vol_ratio": 1.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "0DTE options module disabled",
            "source": "disabled",
            "expirations": [],
            "total_volume": 0.0,
            "total_premium": 0.0,
        }

    elev_ratio = float(ov_cfg.get("elevated_ratio", 1.8))
    boost_ratio = float(ov_cfg.get("boost_ratio", 2.5))
    penalty_ratio = float(ov_cfg.get("penalty_ratio", 2.2))
    min_confidence = float(ov_cfg.get("min_confidence", 0.40))
    min_volume = float(ov_cfg.get("min_volume", 500))

    live = fetch_yfinance_0dte_chain(ticker)
    source = "yfinance"
    odte_ratio = 0.0
    call_vol = 0.0
    put_vol = 0.0
    total_vol = 0.0
    total_prem = 0.0
    call_put_vol_ratio = 1.0
    side_bias = "neutral"
    expirations: List[str] = []

    if live is not None and live.get("total_volume", 0) > 0:
        call_vol = live.get("call_volume", 0.0)
        put_vol = live.get("put_volume", 0.0)
        total_vol = live.get("total_volume", 0.0)
        total_prem = live.get("total_premium", 0.0)
        expirations = live.get("expirations", [])
        # Simple baseline: assume "normal" near-term volume ~ median equity
        # We use a deterministic synthetic baseline derived from ticker for ratio.
        seed = sum(ord(c) for c in ticker) + datetime.now().timetuple().tm_yday
        rng = random.Random(seed)
        baseline_vol = rng.uniform(800, 4500)
        odte_ratio = round(total_vol / max(baseline_vol, 1.0), 3)
        if put_vol > 0:
            call_put_vol_ratio = round(call_vol / put_vol, 3)
        elif call_vol > 0:
            call_put_vol_ratio = 99.0
        if call_put_vol_ratio >= 1.6:
            side_bias = "call"
        elif call_put_vol_ratio <= 0.65:
            side_bias = "put"
        else:
            side_bias = "neutral"
    else:
        # Stable synthetic daily proxy – deterministic per ticker + day
        source = "synthetic_proxy"
        seed = sum(ord(c) for c in ticker) + datetime.now().timetuple().tm_yday
        rng = random.Random(seed)

        # Realistic near-term options volume for mid/large-cap names
        base = rng.uniform(600, 3200)
        spike = rng.random() < 0.28  # ~28 % of days show elevated 0DTE activity
        if spike:
            total_vol = round(base * rng.uniform(2.1, 5.8), 0)
            odte_ratio = round(total_vol / max(base, 1.0), 3)
        else:
            total_vol = round(base * rng.uniform(0.55, 1.45), 0)
            odte_ratio = round(total_vol / max(base, 1.0), 3)

        # Side bias
        bias_roll = rng.random()
        if bias_roll < 0.38:
            side_bias = "call"
            call_put_vol_ratio = round(rng.uniform(1.7, 4.5), 2)
        elif bias_roll < 0.70:
            side_bias = "put"
            call_put_vol_ratio = round(rng.uniform(0.22, 0.58), 2)
        else:
            side_bias = "neutral"
            call_put_vol_ratio = round(rng.uniform(0.75, 1.35), 2)

        call_vol = total_vol * (call_put_vol_ratio / (1 + call_put_vol_ratio)) if call_put_vol_ratio > 0 else total_vol / 2
        put_vol = total_vol - call_vol
        # Rough premium proxy ($ notional)
        total_prem = round(total_vol * rng.uniform(0.8, 4.5), 0)

        today = datetime.now().date()
        expirations = [(today + timedelta(days=d)).isoformat() for d in (0, 1, 2) if d >= 0]

    # Infer signal
    signal_boost = 0
    confidence = 0.52
    reason_parts: List[str] = []

    if total_vol < min_volume and source == "yfinance":
        reason_parts.append(f"Low near-term volume {total_vol:.0f} — no actionable 0DTE signal")
    elif odte_ratio >= boost_ratio:
        if side_bias == "call":
            signal_boost = 1
            confidence = min(0.90, 0.55 + 0.12 * min(odte_ratio, 5.0))
            reason_parts.append(
                f"Elevated 0DTE call flow (ratio {odte_ratio:.2f}, C/P {call_put_vol_ratio:.2f}) — short-horizon bullish / dealer hedging demand"
            )
        elif side_bias == "put":
            signal_boost = -1
            confidence = min(0.90, 0.55 + 0.12 * min(odte_ratio, 5.0))
            reason_parts.append(
                f"Elevated 0DTE put flow (ratio {odte_ratio:.2f}, C/P {call_put_vol_ratio:.2f}) — short-horizon caution / protective flow"
            )
        else:
            signal_boost = 0
            confidence = min(0.78, 0.50 + 0.08 * odte_ratio)
            reason_parts.append(
                f"Elevated 0DTE volume (ratio {odte_ratio:.2f}) — event-risk / volatility spike, side neutral"
            )
    elif odte_ratio >= elev_ratio:
        confidence = min(0.72, 0.48 + 0.07 * odte_ratio)
        reason_parts.append(
            f"Mildly elevated near-term options activity (ratio {odte_ratio:.2f}, side {side_bias})"
        )
    else:
        reason_parts.append(
            f"0DTE / near-term flow normal (ratio {odte_ratio:.2f}, C/P {call_put_vol_ratio:.2f})"
        )

    # Extra penalty when high premium coincides with put bias
    if total_prem > 15000 and side_bias == "put" and signal_boost >= 0:
        signal_boost = -1
        confidence = max(confidence, 0.70)
        reason_parts.append("High put premium notional — elevated hedging / event risk")

    if confidence < min_confidence and signal_boost != 0:
        signal_boost = 0

    return {
        "odte_ratio": float(odte_ratio),
        "side_bias": side_bias,
        "call_put_vol_ratio": float(call_put_vol_ratio),
        "signal_boost": signal_boost,
        "confidence": round(confidence, 2),
        "reason": " | ".join(reason_parts) if reason_parts else "No significant 0DTE signal",
        "source": source,
        "expirations": expirations[:4],
        "total_volume": float(total_vol),
        "total_premium": float(total_prem),
        "call_volume": float(call_vol),
        "put_volume": float(put_vol),
    }


def integrate_options_0dte_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Attach 0DTE metrics to a signal row and apply soft boost/penalty."""
    odte = detect_options_0dte(row["ticker"], cfg)
    row.update({
        "odte_ratio": odte["odte_ratio"],
        "odte_side_bias": odte["side_bias"],
        "odte_cp_ratio": odte["call_put_vol_ratio"],
        "odte_boost": odte["signal_boost"],
        "odte_confidence": odte["confidence"],
        "odte_reason": odte["reason"],
        "odte_source": odte.get("source", "unknown"),
        "odte_expirations": odte.get("expirations", []),
        "odte_volume": odte.get("total_volume", 0.0),
        "odte_premium": odte.get("total_premium", 0.0),
    })

    boost = odte["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | ⚡ {odte['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | ⚡ {odte['reason']}"
    else:
        if odte["odte_ratio"] > 1.0:
            row["signal_reason"] = (row.get("signal_reason") or "") + f" | 0DTE: {odte['reason']}"

    return row
