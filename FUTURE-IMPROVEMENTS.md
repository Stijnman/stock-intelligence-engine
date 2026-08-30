# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## High Priority

- [ ] **Narrative Graph / Conversation Network Intelligence**. Build a lightweight graph of actors, themes, and contagion edges from X/Reddit/YouTube so the engine can surface "who is talking about what and how narratives spread" instead of isolated velocity scores.
- [ ] **Options Vanna / Charm / DEX Exposure Overlay**. Extend options surface beyond IV skew and 0DTE volume to dealer vanna/charm/DEX positioning for short-horizon flow prediction.
- [ ] **Earnings Call Transcript Diff & Guidance Change Detector**. Diff consecutive earnings transcripts (and 10-Q/10-K Risk Factors) for material language changes, guidance shifts, and tone deltas; soft-boost/penalty on watchlist when management language moves against or with the current narrative.
- [ ] **Native MCP Server for Agent Integration**. Expose the full analysis pipeline (watchlist signals, thesis pairs, overlays, backtest) as an MCP server so Claude / Grok / custom agents can call `analyze_ticker`, `get_thesis`, `run_report` natively without custom glue.
- [ ] **Company Digital Footprint Momentum Overlay (Web Traffic + App Downloads)**. AltIndex-style forward demand proxy using company website traffic trends and consumer app download/engagement momentum as leading indicators of revenue and narrative durability.
- [ ] **Satellite Imagery / Geolocation Foot-Traffic & Parking Activity Overlay**. Earth-observation derived proxies (car counts, store/parking occupancy, night lights) as real-economy activity confirmation for retail, industrial and consumer names; soft boost when activity diverges positively from pure narrative heat.
- [ ] **AI Token Consumption / AI Premium Factor Overlay**. Track firm-level or sector exposure to realized AI token usage growth (OpenRouter-style intensive margin) and compute an AI-beta style premium signal; useful for identifying names that benefit from or are disrupted by frontier AI adoption.
- [x] **Market Regime Adaptive Overlay Weighting** (completed 2026-08-28, v2.25.0). Dynamically re-weight technical, narrative, flow and fundamental overlays according to current market regime (VIX terciles, trend strength, realized volatility); reduce narrative weight in high-vol regimes and increase flow/technical weight when trends are strong. Fully wired in `sie/regime.py` + analyzer + CLI + dashboard + config.
- [x] **Semiconductor / AI Supply-Chain CapEx Momentum Tracker** (completed 2026-08-28, v2.26.0). Monitor order trends, backlog commentary and CapEx guidance from key AI infrastructure suppliers (ASML, AMAT, LRCX, KLAC, TSM). Fully wired in `sie/supply_chain.py` + analyzer + CLI (`--no-supply-chain`) + dashboard + config. Uses yfinance peek when available, otherwise labeled synthetic proxy.
- [x] **Authenticity-Filtered Social Narrative Velocity Overlay** (completed 2026-08-29, v2.27.0). Score individual X/Reddit posts for authenticity / bot-likelihood / spam risk before aggregating velocity and sentiment; surface only high-authenticity narrative heat. Reduces 2026-era coordinated retail manipulation noise that pure volume/mention metrics cannot filter. Fully wired in `sie/authenticity.py` + analyzer + CLI (`--no-authenticity`) + dashboard + config. Uses labeled deterministic synthetic proxy; live bot-classifier hook left explicit.
- [ ] **Earnings Call Q&A vs Prepared Remarks Sentiment & Guidance Divergence Detector**. Segment transcripts into management prepared remarks vs analyst Q&A; detect tone, hedging, and guidance language shifts specific to pressure questions. Soft boost/penalty when Q&A diverges materially from prepared narrative.
- [ ] **Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay**. Use anonymized panel or public proxy spend data (category, merchant, geography) as a leading revenue nowcast for retail, restaurant, travel and consumer names; soft boost when spend momentum diverges positively from pure narrative or hiring signals.
- [ ] **Maritime AIS / Port Congestion & Vessel Activity Overlay**. Track AIS-derived port dwell times, vessel counts and congestion indices for key logistics, energy and industrial names as a real-economy activity confirmation; soft boost/penalty when physical flow diverges from narrative heat.

## Medium Priority

- [ ] **Options Max Pain & Open-Interest Wall Detector**. Surface max-pain levels and large OI walls as soft context for short-horizon signals.
- [ ] **Pre-Market Theme Rotation & Volume Surge Scanner**. Detect unusual pre-market volume + theme keyword spikes to flag potential narrative rotation before the open.
- [ ] **Cross-Ticker Narrative Contagion Detector**. Measure when attention or sentiment on one ticker rapidly transfers to correlated names inside the same theme.
- [x] **Wikipedia / Google Trends Attention Momentum Tracker** (completed 2026-08-28, v2.26.0). Use pageview / search interest momentum as an early retail-attention proxy. Fully wired in `sie/attention.py` + analyzer + CLI (`--no-attention`) + dashboard + config. Wikimedia pageviews when reachable, else synthetic proxy.
- [ ] **Patent Filing & IP Momentum Overlay**. Track recent patent grants and applications as a forward-looking R&D / moat signal for tech names.
- [ ] **Government Contract & Lobbying Activity Overlay**. Surface material new contracts or lobbying spikes (Quiver-style) as soft fundamental confirmation.
- [x] **FINRA Short Volume / Short Interest Momentum Overlay** (completed 2026-08-28, v2.26.0). Ingest daily FINRA short-volume ratios and short-interest changes; treat elevated short volume against a rising narrative as a caution flag and short covering as a potential boost. Fully wired in `sie/short_interest.py` + analyzer + CLI (`--no-short-interest`) + dashboard + config. Current source is a labeled synthetic proxy; live FINRA CSV is an explicit future hook.
- [ ] **YouTube Finance Creator Sentiment Overlay**. Treat major finance YouTube channels and ticker-specific video comments as a first-class sentiment source (alongside X and Reddit) with per-video and aggregate scores.
- [ ] **Employee Glassdoor / Outlook Sentiment Tracker**. Use aggregated employee business-outlook and CEO-approval trends as a soft leading indicator of internal confidence (AltIndex-style).
- [ ] **Agentic Multi-Perspective Signal Debate Layer**. Lightweight multi-agent loop that generates independent bull, bear, and neutral readings then produces a short consensus or dissent summary before the final signal is emitted.
- [x] **Streamlit Fragment Live Dashboard Refresh** (completed 2026-08-26, v2.23.0). Upgrade the dashboard to use `@st.fragment(run_every=...)` for selective real-time updates of price/quote and key overlay cards without full-script reruns, leveraging Streamlit 1.37+ / 1.61 patterns. Fully wired in `app.py` with config-driven interval, cached analysis, live status metrics and Force Full Refresh.
- [x] **Signal Confidence Calibration & LLM Self-Critique Layer** (completed 2026-08-28, v2.24.0). Post-signal self-critique that scores consistency across overlays and flags over-confident or conflicting signals before they reach the dashboard or alerts. Fully wired in `sie/confidence.py` + analyzer orchestration + CLI + dashboard columns.
- [ ] **Cross-Platform Social Follower Growth Momentum**. Track follower count velocity across X, Instagram, TikTok, Threads and StockTwits as a durable attention / brand-momentum signal (AltIndex-style social signals).
- [ ] **Dual-Score News Impact vs Tone Detector**. Separate pure linguistic sentiment from estimated short-term price-impact potential (Rhea-AI / StockTitan style) so high-impact neutral headlines and low-impact hype can be treated differently.
- [ ] **Stratified Multi-Agent Research Report Generator**. Expand beyond thesis + brief into a full stratified report (facts vs inference vs disclaimer) with explicit evidence citations and multi-agent role specialization (news, fundamentals, technical, risk).
- [ ] **Earnings Call Audio Tone & Prosody Sentiment Layer**. Beyond pure transcript text, extract audio-level cues (speaking rate, pitch variance, hesitation markers) from earnings calls via Whisper + prosody models to detect management confidence or stress not fully captured in words.
- [ ] **Vision-Model Chart Pattern & Anomaly Detector**. Apply a lightweight multimodal / vision model to recent price/volume charts to flag classical patterns, divergences or visual anomalies that pure numeric indicators miss; surface as soft context.
- [ ] **Open-Source Factor Risk Decomposition Overlay**. Attribute the current signal and returns to public factor exposures (value, momentum, quality, low-vol, AI-beta style) using open factor libraries or data so users can see style bets embedded in the watchlist.
- [ ] **Dealer Gamma Exposure (GEX) Real-Time Overlay**. Estimate net dealer gamma positioning from options chain data; surface short-horizon mean-reversion vs trend-acceleration bias as a soft flow overlay complementary to existing IV skew / 0DTE / Vanna-Charm work.
- [ ] **Multi-User Persistent Watchlist & Session Sync for Streamlit**. Add lightweight auth-backed (or local encrypted) persistent watchlists, multi-page architecture, and cross-session state so users can save/share configurations and avoid full re-entry on every dashboard load.
- [ ] **Cloud Deployment Profiles & Production Auth Templates**. Ship ready-to-use Docker / Streamlit Community Cloud / Cloudflare Access / PandaStack-style configs plus secrets management and scale-to-zero guidance so private production dashboards are one-command deployable.
- [ ] **Substack & Independent Research Newsletter Sentiment Overlay**. Treat high-signal finance Substacks and independent research newsletters as a first-class narrative source; score tone, conviction and revision language per author/publication and aggregate into a soft overlay.
- [ ] **Analyst Estimate Revision Momentum & Surprise Probability Overlay**. Track the velocity and direction of consensus EPS/revenue revisions (and free public estimate sources) as a leading fundamental confirmation signal; soft boost when revisions accelerate in the direction of the current narrative.
- [ ] **Order-Flow / Level-2 Imbalance Soft Overlay**. Use public or low-latency proxies for order-book imbalance and aggressive buy/sell pressure as a short-horizon microstructure confirmation layer complementary to dark-pool and 0DTE flow.

## Long-Term / Nice-to-Have

- [ ] Historical narrative database with winner/loser attribution.
- [ ] Full local LLM agent ("What's the inference trade right now?").
- [ ] Multi-theme watchlist packs and theme rotation engine.
- [ ] Plugin architecture for third-party overlays.
- [ ] Truth Social / high-influence political narrative feed for market-moving accounts.
- [ ] Economic moat + AI-impact scoring layer (MoatScan-style).

Last updated: 2026-08-30 (v2.27.1 — Autonomous research & evolution cycle; five new roadmap items added)
