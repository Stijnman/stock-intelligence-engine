"""Streamlit dashboard — colorful, interactive stock intelligence UI."""

from __future__ import annotations

import streamlit as st

from sie.analyzer import analyze_watchlist, format_report
from sie.charts import (
    SIGNAL_COLORS,
    drawdown_chart,
    price_ma_chart,
    rsi_gauge,
    signal_bar_chart,
    signal_donut,
)
from sie.config import load_config
from sie.export import export_csv
from sie.i18n import t, translate_reason

# ── Page & theme ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Stock Intelligence Engine",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded",
)

SIGNAL_BADGE = {
    "strong_buy": ("STRONG", "#00E676", "#003d20"),
    "buy": ("BUY", "#18FFFF", "#003d4d"),
    "hold": ("HOLD", "#FFD740", "#4d3d00"),
    "caution": ("CAUTION", "#FF5252", "#4d0000"),
}

FIT_COLORS = {"strong": "#00E676", "monitor": "#FFD740", "weak": "#FF5252"}

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a0a2e 0%, #16213e 40%, #0f3460 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(124, 77, 255, 0.35);
    box-shadow: 0 8px 32px rgba(124, 77, 255, 0.15);
}
.hero h1 {
    background: linear-gradient(90deg, #7C4DFF, #18FFFF, #00E676);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0;
}
.hero p { color: #b0bec5; margin: 0.5rem 0 0; font-size: 1.05rem; }

.metric-card {
    background: linear-gradient(145deg, #1a1f2e 0%, #12151f 100%);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(124, 77, 255, 0.2);
}
.metric-label { color: #90a4ae; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-value { font-size: 1.8rem; font-weight: 700; margin: 0.3rem 0; }
.metric-sub { color: #78909c; font-size: 0.85rem; }

.signal-pill {
    display: inline-block;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
}

.chart-panel {
    background: linear-gradient(160deg, #151a28 0%, #0e1117 100%);
    border-radius: 18px;
    padding: 1rem 1.2rem 0.5rem;
    border: 1px solid rgba(124, 77, 255, 0.12);
    margin-bottom: 1rem;
}

.ticker-tab-card {
    background: #1a1f2e;
    border-radius: 14px;
    padding: 1.2rem;
    border-left: 4px solid #7C4DFF;
    margin-bottom: 0.8rem;
}

.headline-chip {
    background: rgba(24, 255, 255, 0.08);
    border: 1px solid rgba(24, 255, 255, 0.2);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    color: #cfd8dc;
    font-size: 0.9rem;
}

.disclaimer-bar {
    background: linear-gradient(90deg, rgba(255,82,82,0.15), rgba(255,215,64,0.1));
    border: 1px solid rgba(255,215,64,0.25);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    color: #ffcc80;
    font-size: 0.85rem;
    text-align: center;
    margin-top: 2rem;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e1117 0%, #1a1035 100%);
}
div[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(90deg, #7C4DFF, #536dfe);
    border: none;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(90deg, #9575ff, #7C4DFF);
    box-shadow: 0 4px 20px rgba(124, 77, 255, 0.4);
}

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: #1a1f2e;
    border-radius: 10px 10px 0 0;
    padding: 10px 20px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #2d1f5e, #1a1f2e);
    color: #18FFFF !important;
}
</style>
""",
    unsafe_allow_html=True,
)


def signal_badge_html(signal: str, lang: str) -> str:
    label, fg, bg = SIGNAL_BADGE.get(signal, SIGNAL_BADGE["hold"])
    label = t(lang, signal)
    return (
        f'<span class="signal-pill" style="background:{bg};color:{fg};'
        f'border:1px solid {fg}40;">{label}</span>'
    )


def render_metric_card(label: str, value: str, sub: str = "", accent: str = "#7C4DFF") -> str:
    return f"""
    <div class="metric-card" style="border-top: 3px solid {accent};">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{accent};">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """


def render_ticker_card(row: dict, lang: str) -> None:
    signal = row.get("signal", "hold")
    accent = SIGNAL_COLORS.get(signal, "#FFD740")
    price = f"${row['price']:,.2f}" if row.get("price") is not None else "—"
    rsi = row.get("rsi", "—")
    dd = row.get("drawdown_pct", "—")
    reason = translate_reason(row.get("signal_reason", ""), lang)

    st.markdown(
        f"""
        <div class="ticker-tab-card" style="border-left-color:{accent};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-size:1.5rem;">{row.get('color', '')}</span>
                    <strong style="font-size:1.3rem;margin-left:0.5rem;">{row['ticker']}</strong>
                    <span style="color:#90a4ae;margin-left:0.5rem;">{row['name']}</span>
                </div>
                {signal_badge_html(signal, lang)}
            </div>
            <p style="color:#b0bec5;margin:0.8rem 0 0.3rem;">{row.get('note', '')}</p>
            <p style="color:#78909c;font-size:0.9rem;margin:0;">{reason}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_metric_card(t(lang, "price"), price, accent=accent), unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric_card("RSI", str(rsi), "14-period", accent="#7C4DFF"), unsafe_allow_html=True)
    with c3:
        st.markdown(
            render_metric_card(t(lang, "drawdown"), f"{dd}%", "from 52w high", accent="#FF5252"),
            unsafe_allow_html=True,
        )
    with c4:
        fit = row.get("narrative_fit", "monitor")
        st.markdown(
            render_metric_card("Narrative fit", fit.upper(), row.get("theme", ""), accent=FIT_COLORS.get(fit, "#FFD740")),
            unsafe_allow_html=True,
        )

    col_chart, col_gauge = st.columns([2, 1])
    with col_chart:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(price_ma_chart(row["ticker"]), use_container_width=True, key=f"price_{row['ticker']}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_gauge:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(rsi_gauge(row.get("rsi"), row["ticker"]), use_container_width=True, key=f"rsi_{row['ticker']}")
        st.markdown("</div>", unsafe_allow_html=True)

    if row.get("headlines"):
        st.markdown(f"**{t(lang, 'news')}**")
        for h in row["headlines"]:
            st.markdown(f'<div class="headline-chip">📰 {h}</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────

cfg = load_config()

with st.sidebar:
    st.markdown("### ⚙️ Controls")
    lang = st.selectbox("Language", ["en", "nl"], format_func=lambda x: "English" if x == "en" else "Nederlands")
    include_news = st.checkbox("Include headlines", value=True)
    auto_export = st.checkbox("Export CSV on analyze", value=False)
    show_text_report = st.checkbox("Show text report", value=False)

    st.markdown("---")
    st.markdown("### 📊 Watchlist")
    for ticker, meta in cfg.get("tickers", {}).items():
        st.markdown(f"{meta.get('color', '🟡')} **{ticker}** — {meta.get('name', ticker)}")

    st.markdown("---")
    run = st.button("🚀 Analyze watchlist", type="primary", use_container_width=True)

# ── Hero ──────────────────────────────────────────────────────────────────────

theme = cfg.get("narrative", {}).get("theme", "AI Inference Boom")
st.markdown(
    f"""
    <div class="hero">
        <h1>📈 Stock Intelligence Engine</h1>
        <p>Narrative theme: <strong style="color:#18FFFF;">{theme}</strong> · v2.0.0</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────

if "report" not in st.session_state:
    st.session_state.report = None

if run:
    with st.spinner("Fetching prices, computing signals…"):
        st.session_state.report = analyze_watchlist(cfg, include_news=include_news, lang=lang)

report = st.session_state.report

if report is None:
    st.markdown(
        """
        <div style="text-align:center;padding:4rem 2rem;color:#78909c;">
            <div style="font-size:4rem;margin-bottom:1rem;">🎯</div>
            <h3 style="color:#b0bec5;">Ready to analyze</h3>
            <p>Hit <strong style="color:#7C4DFF;">Analyze watchlist</strong> in the sidebar to load live data and charts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    rows = report["rows"]
    ts = report.get("timestamp", "")

    # Summary metrics
    signals = [r.get("signal", "hold") for r in rows]
    strong = sum(1 for s in signals if s == "strong_buy")
    buys = sum(1 for s in signals if s == "buy")
    holds = sum(1 for s in signals if s == "hold")
    cautions = sum(1 for s in signals if s == "caution")

    st.caption(f"🕐 {t(lang, 'updated')}: **{ts}**")

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(render_metric_card("Tickers", str(len(rows)), "in watchlist", "#18FFFF"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric_card("Strong", str(strong), "signals", "#00E676"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric_card("Buy", str(buys), "signals", "#18FFFF"), unsafe_allow_html=True)
    with m4:
        st.markdown(render_metric_card("Hold", str(holds), "signals", "#FFD740"), unsafe_allow_html=True)
    with m5:
        st.markdown(render_metric_card("Caution", str(cautions), "signals", "#FF5252"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Overview charts
    chart_left, chart_mid, chart_right = st.columns([2, 1, 1])
    with chart_left:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(signal_bar_chart(rows), use_container_width=True, key="signal_bars")
        st.markdown("</div>", unsafe_allow_html=True)
    with chart_mid:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(signal_donut(rows), use_container_width=True, key="signal_donut")
        st.markdown("</div>", unsafe_allow_html=True)
    with chart_right:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(drawdown_chart(rows), use_container_width=True, key="drawdown_bars")
        st.markdown("</div>", unsafe_allow_html=True)

    # Interactive ticker tabs
    tab_labels = [f"{r.get('color', '')} {r['ticker']}" for r in rows]
    tabs = st.tabs(tab_labels)
    for tab, row in zip(tabs, rows):
        with tab:
            render_ticker_card(row, lang)

    # Data table with styling
    st.markdown("### 📋 Full watchlist")
    display = [
        {
            "Ticker": r["ticker"],
            "Name": r["name"],
            "Price": f"${r['price']:,.2f}" if r.get("price") else "—",
            "RSI": r.get("rsi"),
            "MA50": r.get("ma50"),
            "MA200": r.get("ma200"),
            "52w DD%": r.get("drawdown_pct"),
            "Signal": t(lang, r.get("signal", "hold")),
            "Fit": r.get("narrative_fit"),
        }
        for r in rows
    ]
    st.dataframe(display, use_container_width=True, hide_index=True)

    if show_text_report:
        with st.expander("Text report"):
            st.code(format_report(report), language=None)

    if auto_export and run:
        flat = [{k: v for k, v in r.items() if k != "headlines"} for r in rows]
        path = export_csv(flat, cfg.get("export", {}).get("directory", "exports"))
        st.success(f"Exported {path}")

st.markdown(
    f'<div class="disclaimer-bar">⚠️ {t(lang if report else "en", "disclaimer")}</div>',
    unsafe_allow_html=True,
)