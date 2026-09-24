# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.40.1] - 2026-09-24

### Research & Evolution
- Executed the full autonomous research & evolution cycle against `main` @ 404b8c09 / follow-on version bump commit.
- Code audit confirmed **KOL / Influencer Narrative Amplification** is fully wired (`sie/kol_amplification.py`, analyzer `include_kol_amplification`, CLI `--no-kol-amplification`, config `kol_amplification:`). Removed from FUTURE-IMPROVEMENTS.md High Priority (implementation shipped in v2.40.0; roadmap was lagging).
- Dashboard `__version__` and preferred-column list were still on 2.39.2 and omitted `kol_*` — aligned to 2.40.1.
- Fresh 2026 research: SentiSense / Adanos multi-source sentiment + MCP for agents, StockTitan Rhea-AI materiality/impact scoring, OpenAI ChatGPT for Financial Services (Daloopa / LSEG transcripts), NorrisAI AlphaLens live-filing frameworks, NowNews honesty-signal news intelligence, CFTC COT crowding, FDA/PDUFA calendars, dual-listed ADR basis, labor CBA expiries, ADS-B executive-travel nowcasts.
- Added five non-duplicate roadmap overlays:
  - **FDA / Clinical-Trial Milestone & Protocol-Amendment Velocity Overlay** (High Priority)
  - **CFTC Commitment-of-Traders Speculative Positioning Overlay** (High Priority)
  - **Labor-Action / Collective-Bargaining Expiry Overlay** (Medium Priority)
  - **Dual-Listed ADR / Ordinary-Share Basis Overlay** (Medium Priority)
  - **Corporate-Jet / Executive-Travel Nowcast Overlay** (Long-Term)

### Version
- Aligned package, CLI, dashboard and docs to **2.40.1**.
- Patch bump: roadmap/docs/version metadata + dashboard column alignment; no new runtime overlay module in this commit.

### Notes
- Educational research tool only — not financial advice.

---

## [2.40.0] - 2026-09-23

### Added
- **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`).
  Scores high-follower / high-engagement authentic accounts and amplification cascades across X / Reddit / YouTube proxies.
  Soft +1 when organic KOL-driven velocity confirms an authentic narrative; soft -1 on coordinated or low-authenticity amplification spikes.
  Wired through analyzer (`include_kol_amplification`), CLI (`--no-kol-amplification`), config (`kol_amplification:`), Streamlit preferred columns (`kol_score`, `kol_cascade`, `kol_amp_ratio`, `kol_auth`, `kol_boost`, `kol_reason`).
  Deterministic synthetic proxy when live follower-graph feeds are unavailable.

### Version
- Package, CLI, dashboard and docs aligned to **2.40.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.39.2] - 2026-09-23

### Research & Evolution
- Executed the full `AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md` against `main`.
- Verified every open `FUTURE-IMPROVEMENTS.md` concept against the current `sie/` module tree. **No open roadmap item satisfies the complete wiring gate** at that cut, so none was removed then.
- Added five non-duplicate roadmap overlays (index reconstitution, listed earnings event-contracts, working-capital DSO/DIO, SaaS status-page incidents, CAT-bond / ROL).

### Version
- Aligned package, CLI, dashboard and docs to **2.39.2**.

---

See git history for 2.39.1 and earlier releases.

*Educational research tool only — not financial advice.*
