"""Regression tests for Stock Intelligence Engine's public interfaces."""

import inspect
import sys

import sie
import stock_intelligence_engine as cli
from sie.analyzer import analyze_watchlist, run_report


def test_public_exports_resolve_to_real_symbols():
    missing = [name for name in getattr(sie, "__all__", []) if not hasattr(sie, name)]
    assert not missing, f"Unresolved public exports: {missing}"


def test_report_accepts_0dte_option_from_cli():
    parameters = inspect.signature(run_report).parameters
    assert "include_options_0dte" in parameters


def test_watchlist_accepts_0dte_option_from_report_runner():
    parameters = inspect.signature(analyze_watchlist).parameters
    assert "include_options_0dte" in parameters


def test_new_overlay_flags_on_watchlist_and_report():
    for fn in (analyze_watchlist, run_report):
        params = inspect.signature(fn).parameters
        assert "include_supply_chain" in params
        assert "include_short_interest" in params
        assert "include_attention" in params
        assert "include_authenticity" in params
        assert "include_confidence" in params
        assert "include_regime" in params


def test_report_forwards_new_overlay_flags(monkeypatch):
    captured = {}

    def fake_watchlist(*args, **kwargs):
        captured.update(kwargs)
        return {"rows": []}

    monkeypatch.setattr("sie.analyzer.analyze_watchlist", fake_watchlist)
    run_report(
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
        include_supply_chain=False,
        include_short_interest=False,
        include_attention=False,
        include_authenticity=False,
    )

    assert captured["include_supply_chain"] is False
    assert captured["include_short_interest"] is False
    assert captured["include_attention"] is False
    assert captured["include_authenticity"] is False


def test_report_forwards_0dte_option_to_watchlist(monkeypatch):
    captured = {}

    def fake_watchlist(*args, **kwargs):
        captured.update(kwargs)
        return {"rows": []}

    monkeypatch.setattr("sie.analyzer.analyze_watchlist", fake_watchlist)
    run_report(
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
    report = {"rows": [{"ticker": "SIE"}]}
    export_path = tmp_path / "report.csv"

    monkeypatch.setattr("sie.analyzer.analyze_watchlist", lambda *args, **kwargs: report)
    monkeypatch.setattr("sie.export.export_csv", lambda rows, directory: export_path)

    result = run_report(
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
    captured = {}
    monkeypatch.setattr(cli, "run_report", lambda **kwargs: captured.update(kwargs) or {})
    monkeypatch.setattr(sys, "argv", ["stock_intelligence_engine.py", "--export"])

    cli.main()

    assert captured["export"] is True


def test_cli_forwards_new_overlay_disables(monkeypatch):
    captured = {}
    monkeypatch.setattr(cli, "run_report", lambda **kwargs: captured.update(kwargs) or {})
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "stock_intelligence_engine.py",
            "--no-supply-chain",
            "--no-short-interest",
            "--no-attention",
            "--no-authenticity",
        ],
    )

    cli.main()

    assert captured["include_supply_chain"] is False
    assert captured["include_short_interest"] is False
    assert captured["include_attention"] is False
    assert captured["include_authenticity"] is False
