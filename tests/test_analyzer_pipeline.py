"""Regression coverage for unified analysis and CLI/Docker-compatible flags."""
from __future__ import annotations

import csv
import sys

import pytest

from sie import analyzer
from sie.config import DEFAULT_CONFIG, load_config
import stock_intelligence_engine as cli


def test_config_returns_independent_nested_defaults(tmp_path, monkeypatch):
    first = load_config(tmp_path / "missing.yaml")
    first["tokenized_equity_premium"]["enabled"] = False
    second = load_config(tmp_path / "missing.yaml")
    assert second["tokenized_equity_premium"]["enabled"] is True
    assert DEFAULT_CONFIG["tokenized_equity_premium"]["enabled"] is True


def test_run_report_honors_disabled_overlay_and_config_watchlist(monkeypatch):
    cfg = {
        "tickers": {"AAPL": {}},
        "tokenized_equity_premium": {"enabled": False},
        "agentic_mcp_tool_call_latency": {"enabled": True},
        "expert_network_call_novelty": {"enabled": False},
        "signed_options_flow_toxicity": {"enabled": True},
        "unified_multi_source_narrative_freshness": {"enabled": False},
    }
    report = analyzer.run_report(config=cfg)
    row = report["rows"][0]
    assert report["overlays"] == ["oft", "mcp"]
    assert row["tep_status"] == "disabled"
    assert row["enc_status"] == "disabled"
    assert row["ums_status"] == "disabled"
    assert row["overlay_data_mode"] == "synthetic_proxy"


def test_run_report_attaches_investment_analysis(monkeypatch):
    monkeypatch.setattr(
        "sie.investment.analyst.analyze_stock",
        lambda ticker: {"ticker": ticker, "market": {"price": 123.0}, "valuation": {"status": "unavailable"}},
    )
    report = analyzer.run_report(config={"tickers": {"AAPL": {}}}, include_investment=True)
    assert report["investment_analysis"]["AAPL"]["market"]["price"] == 123.0


def test_run_report_investment_failure_isolated(monkeypatch):
    def fail(_ticker):
        raise RuntimeError("provider offline")
    monkeypatch.setattr("sie.investment.analyst.analyze_stock", fail)
    report = analyzer.run_report(config={"tickers": {"AAPL": {}}}, include_investment=True)
    assert report["investment_analysis"]["AAPL"]["status"] == "unavailable"
    assert "provider offline" in report["investment_analysis"]["AAPL"]["error"]


def test_export_creates_csv(tmp_path):
    report = analyzer.run_report(
        config={"tickers": {"AAPL": {}}},
        export=True,
        export_dir=tmp_path,
    )
    with open(report["export_path"], newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]["ticker"] == "AAPL"


def test_cli_accepts_compose_arguments(monkeypatch, tmp_path, capsys):
    captured = {}
    monkeypatch.setattr(cli, "load_config", lambda: {"tickers": {"AAPL": {}}})
    def fake_run_report(**kwargs):
        captured.update(kwargs)
        return {"rows": [{"ticker": "AAPL"}], "overlays": [], "export_path": str(tmp_path / "x.csv")}
    monkeypatch.setattr(cli, "run_report", fake_run_report)
    assert cli.main(["--news", "--export", "--no-investment", "--output-dir", str(tmp_path)]) == 0
    assert captured["include_news"] is True
    assert captured["export"] is True
    assert captured["include_investment"] is False
    assert "CSV export" in capsys.readouterr().out
