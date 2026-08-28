# Contributing

## Overlay contract

New signal overlays must ship **fully wired** or not at all:

1. `sie/<name>.py` with `detect_*` + `integrate_*_to_row`
2. `config.yaml` section (`enabled`, thresholds, `min_confidence`)
3. `analyze_watchlist` + `run_report` kwargs + call site
4. CLI `--no-<name>` flag forwarded from `stock_intelligence_engine.py`
5. Dashboard preferred columns in `app.py`
6. Tests: signature + `run_report` forwarding
7. Docs: CHANGELOG, README Recent Edits, FUTURE checkbox, version aligned

Label data `source="synthetic_proxy"` or `source="public_<api>"`. Soft boost only (`-1/0/+1`).

## Process

- Implementation cycles ship at most 3 overlays.
- Research cycles only touch the roadmap.
- Do not claim a feature complete if analyzer/CLI/dashboard wiring is missing.
