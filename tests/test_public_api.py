"""Regression tests for the current public report and CLI interfaces."""

import sys

import pytest

import stock_intelligence_engine as cli
from sie.analyzer import run_report


def test_run_report_returns_current_public_contract(monkeypatch):
    monkeypatch.setattr("sie.analyzer.load_config", lambda: {"tickers": {"AAPL": {}}})

    result = run_report()

    assert result["version"] == "2.78.0"
    assert result["overlays"] == ["ums", "oft", "enc", "mcp", "tep"]
    assert len(result["rows"]) == 1
    assert result["rows"][0]["ticker"] == "AAPL"


def test_report_rows_include_each_overlay_output(monkeypatch):
    monkeypatch.setattr("sie.analyzer.load_config", lambda: {"tickers": {"MSFT": {}}})

    row = run_report()["rows"][0]

    expected = {
        "ums_vel", "ums_sources_ok", "ums_boost", "ums_reason",
        "oft_toxicity", "oft_informed_prob", "oft_boost", "oft_reason",
        "enc_novelty", "enc_sent_vel", "enc_boost", "enc_reason",
        "mcp_latency_ms", "mcp_success_rate", "mcp_boost", "mcp_reason",
        "tep_basis_bps", "tep_24_5_vol_share", "tep_boost", "tep_reason",
    }
    # The current freshness overlay exports ums_fresh_s rather than ums_vel.
    expected.remove("ums_vel")
    expected.add("ums_fresh_s")
    assert expected <= row.keys()


def test_cli_help_exits_successfully(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stock_intelligence_engine.py", "--help"])

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert exc.value.code == 0
    assert "Stock Intelligence Engine" in capsys.readouterr().out
