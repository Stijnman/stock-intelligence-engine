"""Minimal EN/NL UI strings."""

from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "title": "Stock Intelligence Engine",
        "theme": "Narrative theme",
        "updated": "Updated",
        "signal": "Signal",
        "price": "Price",
        "rsi": "RSI",
        "drawdown": "52w drawdown",
        "news": "Recent headlines",
        "disclaimer": "DISCLAIMER: This is NOT financial advice. Educational use only.",
        "strong_buy": "STRONG",
        "buy": "BUY",
        "hold": "HOLD",
        "caution": "CAUTION",
        "no_data": "No data",
    },
    "nl": {
        "title": "Stock Intelligence Engine",
        "theme": "Narratief thema",
        "updated": "Bijgewerkt",
        "signal": "Signaal",
        "price": "Prijs",
        "rsi": "RSI",
        "drawdown": "52w daling",
        "news": "Recente headlines",
        "disclaimer": "DISCLAIMER: Dit is GEEN financieel advies. Alleen educatief.",
        "strong_buy": "STERK",
        "buy": "KOOP",
        "hold": "HOUD",
        "caution": "VOORZICHTIG",
        "no_data": "Geen data",
    },
}


REASON_NL: dict[str, str] = {
    "price > MA50 > MA200": "prijs > MA50 > MA200",
    "price above MA200 only": "alleen boven MA200",
    "below key moving averages": "onder belangrijke gemiddelden",
    "strong narrative fit": "sterke narratief-match",
    "weak narrative fit": "zwakke narratief-match",
    "RSI elevated": "RSI verhoogd",
    "RSI oversold": "RSI oversold",
    "RSI neutral": "RSI neutraal",
    "Insufficient price history": "Onvoldoende koershistorie",
}


def translate_reason(reason: str, lang: str) -> str:
    if lang != "nl":
        return reason
    out = reason
    for en, nl in REASON_NL.items():
        out = out.replace(en, nl)
    return out.replace("(", " (").replace("  ", " ")


def t(lang: str, key: str) -> str:
    return STRINGS.get(lang, STRINGS["en"]).get(key, key)