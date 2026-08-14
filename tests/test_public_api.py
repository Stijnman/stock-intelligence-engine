"""Regression tests for Stock Intelligence Engine's public interfaces."""

import inspect
import sys

import sie
import stock_intelligence_engine as cli


def test_public_exports_resolve_to_real_symbols():
    """Every documented package export must be importable from the package."""
    missing = [name for name in sie.__all__ if not hasattr(sie, name)]
    assert not missing, f"Unresolved public exports: {missing}"


def test_report_accepts_0dte_option_from_cli():
    """The report interface must accept the CLI's 0DTE feature toggle."""
    parameters = inspect.signature(sie.run_report).parameters
    assert "include_options_0dte" in parameters


def test_watchlist_accepts_0dte_option_from_report_runner():
    """The watchlist interface must accept the report runner's 0DTE toggle."""
    parameters = inspect.signature(sie.analyze_watchlist).parameters
    assert "include_options_0dte" in parameters


def test_report_forwards_0dte_option_to_watchlist(monkeypatch):
    """The CLI-facing report runner must forward the 0DTE toggle unchanged."""
    captured = {}

    def fake_watchlist(*args, **kwargs):
        captured.update(kwargs)
        return {"rows": []}

    monkeypatch.setattr("sie.analyzer.analyze_watchlist", fake_watchlist)
    sie.run_report(
        include_news=False,
        include_social=False,
        include_insider=False,
        include_pm=False,
        include_institutional=False,
        include_congressional=False,
        include_realtime=False,
        include_dark_pool=False,
        include_options_iv=False,
        include_options_0dte=False,
    )

    assert captured["include_options_0dte"] is False


def test_report_exports_rows_when_requested(monkeypatch, tmp_path):
    """Requesting an export must persist the produced watchlist rows."""
    report = {"rows": [{"ticker": "SIE"}]}
    export_path = tmp_path / "report.csv"

    monkeypatch.setattr("sie.analyzer.analyze_watchlist", lambda *args, **kwargs: report)
    monkeypatch.setattr("sie.export.export_csv", lambda rows, directory: export_path)

    result = sie.run_report(
        include_news=False,
        include_social=False,
        include_insider=False,
        include_pm=False,
        include_institutional=False,
        include_congressional=False,
        include_realtime=False,
        include_dark_pool=False,
        include_options_iv=False,
        include_options_0dte=False,
        export=True,
        export_dir=tmp_path,
    )

    assert result["export_path"] == str(export_path)


def test_cli_export_switch_is_forwarded(monkeypatch):
    """The command-line export switch must reach the report runner."""
    captured = {}
    monkeypatch.setattr(cli, "run_report", lambda **kwargs: captured.update(kwargs) or {})
    monkeypatch.setattr(sys, "argv", ["stock_intelligence_engine.py", "--export"])

    cli.main()

    assert captured["export"] is True
