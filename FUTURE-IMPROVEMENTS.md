# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## High Priority

- [ ] **Narrative Graph / Conversation Network Intelligence**. Build a lightweight graph of actors, themes, and contagion edges from X/Reddit/YouTube so the engine can surface "who is talking about what and how narratives spread" instead of isolated velocity scores.
- [ ] **Options Vanna / Charm / DEX Exposure Overlay**. Extend options surface beyond IV skew and 0DTE volume to dealer vanna/charm/DEX positioning for short-horizon flow prediction.
- [ ] **Signal Confidence Calibration & LLM Self-Critique Layer**. Post-signal self-critique that scores consistency across overlays and flags over-confident or conflicting signals before they reach the dashboard or alerts.
- [ ] **Earnings Call Transcript Diff & Guidance Change Detector**. Diff consecutive earnings transcripts (and 10-Q/10-K Risk Factors) for material language changes, guidance shifts, and tone deltas; soft-boost/penalty on watchlist when management language moves against or with the current narrative.
- [ ] **Native MCP Server for Agent Integration**. Expose the full analysis pipeline (watchlist signals, thesis pairs, overlays, backtest) as an MCP server so Claude / Grok / custom agents can call `analyze_ticker`, `get_thesis`, `run_report` natively without custom glue.
- [ ] **Narrative vs. Fundamentals Contradiction / Honesty Signal Detector**. Flag cases where multi-source narrative velocity or social sentiment diverges sharply from hard overlays (13F flows, hiring, EDGAR tone, technical structure); surface an "honesty risk" score that penalizes pure-narrative signals.
- [ ] **Company Digital Footprint Momentum Overlay (Web Traffic + App Downloads)**. AltIndex-style forward demand proxy using company website traffic trends and consumer app download/engagement momentum as leading indicators of revenue and narrative durability.

## Medium Priority

- [ ] **Options Max Pain & Open-Interest Wall Detector**. Surface max-pain levels and large OI walls as soft context for short-horizon signals.
- [ ] **Pre-Market Theme Rotation & Volume Surge Scanner**. Detect unusual pre-market volume + theme keyword spikes to flag potential narrative rotation before the open.
- [ ] **Cross-Ticker Narrative Contagion Detector**. Measure when attention or sentiment on one ticker rapidly transfers to correlated names inside the same theme.
- [ ] **Wikipedia / Google Trends Attention Momentum Tracker**. Use pageview / search interest momentum as an early retail-attention proxy.
- [ ] **Patent Filing & IP Momentum Overlay**. Track recent patent grants and applications as a forward-looking R&D / moat signal for tech names.
- [ ] **Government Contract & Lobbying Activity Overlay**. Surface material new contracts or lobbying spikes (Quiver-style) as soft fundamental confirmation.
- [ ] **FINRA Short Volume / Short Interest Momentum Overlay**. Ingest daily FINRA short-volume ratios and short-interest changes; treat elevated short volume against a rising narrative as a caution flag and short covering as a potential boost.
- [ ] **YouTube Finance Creator Sentiment Overlay**. Treat major finance YouTube channels and ticker-specific video comments as a first-class sentiment source (alongside X and Reddit) with per-video and aggregate scores.
- [ ] **Employee Glassdoor / Outlook Sentiment Tracker**. Use aggregated employee business-outlook and CEO-approval trends as a soft leading indicator of internal confidence (AltIndex-style).
- [ ] **Agentic Multi-Perspective Signal Debate Layer**. Lightweight multi-agent loop that generates independent bull, bear, and neutral readings then produces a short consensus or dissent summary before the final signal is emitted.
- [ ] **Streamlit Fragment Live Dashboard Refresh**. Upgrade the dashboard to use `@st.fragment(run_every=...)` for selective real-time updates of price/quote and key overlay cards without full-script reruns, leveraging Streamlit 1.37+ / 1.61 patterns.

## Long-Term / Nice-to-Have

- [ ] Historical narrative database with winner/loser attribution.
- [ ] Full local LLM agent ("What's the inference trade right now?").
- [ ] Multi-theme watchlist packs and theme rotation engine.
- [ ] Plugin architecture for third-party overlays.
- [ ] Truth Social / high-influence political narrative feed for market-moving accounts.
- [ ] Economic moat + AI-impact scoring layer (MoatScan-style).

Last updated: 2026-08-25
