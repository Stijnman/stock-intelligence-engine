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
- [ ] **Near-Instant XBRL Structured Filing Diff & Consensus Surprise Overlay**. Parse structured XBRL from 10-Q/10-K/8-K within seconds of SEC publication (Financial Datasets / similar latency); compute period-over-period metric diffs and surprise vs street consensus; soft boost/penalty on material surprises that confirm or contradict current narrative phase.
- [ ] **Options Liquidity-Ranked Setup Pool & Historical Outcome Tracker**. Rank current unusual options / 0DTE / skew setups by liquidity and historical post-setup return distribution; surface only high-liquidity names with positive expectancy context as soft confirmation for narrative + flow confluence.
- [ ] **Freight Rate & Logistics Cost Index Momentum Overlay**. Track Baltic Dry, container freight indices, and key logistics cost proxies as leading indicators of industrial / consumer goods demand and margin pressure; soft boost when rates confirm rising narrative velocity for cyclicals, caution on cost spikes that contradict bullish narratives.
- [ ] **Job Posting AI-Skill Intensity & Role-Mix Shift Overlay**. Measure company-level job-post volume and the share of postings requiring AI/ML, data-engineering, or frontier-model skills; rising AI-skill intensity as a forward signal of strategic commitment and future CapEx/narrative durability.

## Medium Priority

- [ ] **Options Max Pain & Open-Interest Wall Detector**. Surface max-pain levels and large OI walls as soft context for short-horizon signals.
- [ ] **Pre-Market Theme Rotation & Volume Surge Scanner**. Detect unusual pre-market volume + theme keyword spikes to flag potential narrative rotation before the open.
- [ ] **Cross-Ticker Narrative Contagion Detector**. Measure when attention or sentiment on one ticker rapidly transfers to correlated names inside the same theme. (Note: synthetic proxy module exists in `sie/contagion.py` but is not yet fully wired into analyzer / CLI / dashboard preferred columns.)
- [ ] **Production Streamlit Parquet State Compression + Offline Demo Mode**. Persist dashboard state and cached overlay results in compressed Parquet for fast reloads; ship a fully offline demo mode with synthetic but realistic watchlist so the UI remains usable without live API keys or market hours.
- [ ] **Multi-Provider Sentiment Aggregation Layer with MCP Tool Surface**. Aggregate FinBERT / VADER / external providers (SentiSense, Adanos-style) into a calibrated composite score; expose the aggregation and individual sources as MCP tools for agent consumption.
- [ ] **Retail vs Institutional Options Flow Divergence Gauge**. Separate retail (small-size / high-frequency) vs institutional (block / dark) options activity; flag divergences where retail is chasing a narrative that smart-money flow is fading or confirming.
- [ ] **Expert Network / Third-Party Transcript Sentiment Overlay**. Ingest and score expert-network call transcripts and third-party research notes for tone, conviction, and incremental insight relative to public earnings calls; soft boost when expert consensus confirms or leads public narrative.

## Long-Term / Nice-to-Have

- [ ] Historical narrative database with winner/loser attribution.
- [ ] Full local LLM agent ("What's the inference trade right now?").
- [ ] Multi-theme watchlist packs and theme rotation engine.
- [ ] Plugin architecture for third-party overlays.
- [ ] Truth Social / high-influence political narrative feed for market-moving accounts.
- [ ] Economic moat + AI-impact scoring layer (MoatScan-style).
- [ ] **Cloud Data Marketplace Native Connectors (Snowflake / Databricks / similar)**. Optional read-only connectors that pull curated alternative-data tables or feature stores from cloud marketplaces into the overlay pipeline without leaving the sandbox; keep synthetic-proxy fallback when credentials are absent.
- [ ] **Data-Center Power / Energy Intensity Overlay for AI Infrastructure Names**. Track power-consumption, grid-connection, and energy-intensity proxies for hyperscalers and AI infrastructure names as a physical constraint / CapEx confirmation signal; soft boost when power growth aligns with AI narrative heat.

Last updated: 2026-09-08 (v2.29.5 — Autonomous research & evolution cycle; no completed-item cleanup required; 5 new 2026 high-value items added)
