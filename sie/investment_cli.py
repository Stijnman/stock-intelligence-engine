"""CLI for the free-first Investment Intelligence engine."""
import argparse, json, sys
from pathlib import Path
from sie.investment.analyst import analyze_stock
from sie.investment.etfs import analyze_etf
from sie.investment.portfolio import analyze_portfolio
from sie.investment.providers import quote_and_history
from sie.investment.technical import analyze_history
from sie.investment.data.ecb import euro_reference_rates
from sie.investment.data.eurostat import fetch_dataset
from sie.investment.data.macro import macro_snapshot
from sie.investment.data.nbb import fetch_sdmx_csv, fetch_preset as fetch_nbb_preset, list_presets as list_nbb_presets
from sie.investment.data.worldbank import fetch_indicator
from sie.investment.data.cftc import fetch_legacy_futures_only, positioning_summary
from sie.investment.data.fred import fetch_series as fetch_fred_series
from sie.investment.data.sec_filings import fetch_form4_transactions, fetch_13f_holdings, fetch_reported_earnings_filings
from sie.investment.data.treasury import fetch_debt_to_penny
from sie.investment.advanced import insider_sentiment
from sie.investment.quantitative import analyze_live_portfolio_risk, run_historical_backtest
from sie.investment.data.fsma_uci import fetch_fsma_uci_registry
from sie.investment.belgian_tax import calculate_tob, calculate_net_dividend_yield, calculate_reynders_tax

def main() -> int:
    parser = argparse.ArgumentParser(prog="sie-invest", description="Free-first stock and ETF research")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("analyze", "quote"):
        p = sub.add_parser(name); p.add_argument("ticker")
        if name == "analyze":
            p.add_argument("--macro", action="store_true", help="Attach ECB + Eurostat macro context")
            p.add_argument("--macro-country", default="BE")
            p.add_argument("--macro-currency", default="USD")
    compare = sub.add_parser("compare"); compare.add_argument("tickers", help="Comma-separated ticker symbols")
    portfolio = sub.add_parser("portfolio"); portfolio.add_argument("csv_path", type=Path)
    etf = sub.add_parser("etf"); etf.add_argument("metadata_json", type=Path)
    etf.add_argument("--verify-fsma", action="store_true", help="Verify fund/compartment against the live official FSMA register")
    fsma = sub.add_parser("fsma-uci", help="Search the official FSMA foreign UCI/UCITS register")
    fsma.add_argument("--isin"); fsma.add_argument("--name"); fsma.add_argument("--limit", type=int, default=100)
    tob = sub.add_parser("be-tob", help="Calculate Belgian ETF TOB for one listed secondary-market trade")
    tob.add_argument("amount", type=float); tob.add_argument("--legal-form", choices=["sicav", "fcp"], required=True)
    tob.add_argument("--distribution", choices=["distribution", "capitalisation"], required=True)
    tob.add_argument("--registration", choices=["fsma", "eea", "unregistered", "unknown"], required=True)
    tob.add_argument("--side", choices=["buy", "sell"], default="buy")
    dividend = sub.add_parser("be-net-dividend", help="Estimate Belgian net ETF cash distribution yield")
    dividend.add_argument("--distribution-per-share", type=float, required=True)
    dividend.add_argument("--price", type=float, required=True); dividend.add_argument("--shares", type=float, default=1.0)
    dividend.add_argument("--legal-form", choices=["sicav", "fcp"], required=True)
    dividend.add_argument("--fcp-breakdown", action="store_true", help="A valid fund income breakdown is available")
    dividend.add_argument("--belgian-withholding", type=float, help="Override the calculated default withholding rate")
    dividend.add_argument("--foreign-withholding", type=float, default=0.0)
    fx = sub.add_parser("ecb-fx", help="Fetch free ECB EUR reference exchange rates")
    fx.add_argument("currency", nargs="?", default="USD")
    fx.add_argument("--start"); fx.add_argument("--end")
    eurostat = sub.add_parser("eurostat", help="Fetch a Eurostat dataset")
    eurostat.add_argument("dataset")
    eurostat.add_argument("--filter", action="append", default=[], metavar="DIM=VALUE")
    nbb = sub.add_parser("nbb", help="Fetch an NBB.Stat SDMX CSV API query URL")
    nbb.add_argument("url", help="HTTPS CSV API URL copied from NBB.Stat > API queries")
    nbb_preset = sub.add_parser("nbb-preset", help="Fetch a verified NBB.Stat dataset preset")
    nbb_preset.add_argument("name", nargs="?", help="Preset name; omit to list presets")
    nbb_preset.add_argument("--start-period", default=None, help="Override start period (YYYY or YYYY-MM)")
    wb = sub.add_parser("worldbank", help="Fetch a World Bank Indicators API series")
    wb.add_argument("country", help="ISO country code, e.g. BE, US, DE")
    wb.add_argument("indicator", help="Indicator code, e.g. NY.GDP.MKTP.KD.ZG")
    wb.add_argument("--start", type=int); wb.add_argument("--end", type=int)
    macro = sub.add_parser("macro", help="Fetch free ECB + Eurostat + World Bank macro context")
    macro.add_argument("--country", default="BE")
    macro.add_argument("--currency", default="USD")
    cot = sub.add_parser("cftc-cot", help="Fetch free weekly CFTC Legacy futures-only positioning")
    cot.add_argument("--commodity", help="Commodity name filter, e.g. GOLD or NATURAL GAS")
    cot.add_argument("--start", help="First report date YYYY-MM-DD")
    cot.add_argument("--limit", type=int, default=500)
    fred = sub.add_parser("fred", help="Fetch a FRED series (requires your free FRED_API_KEY)")
    fred.add_argument("series_id", help="FRED series ID, e.g. DFF, CPIAUCSL, UNRATE")
    fred.add_argument("--start"); fred.add_argument("--end")
    sec_insiders = sub.add_parser("sec-insiders", help="Fetch SEC Form 4 insider transactions (requires SEC_USER_AGENT)")
    sec_insiders.add_argument("ticker")
    sec_insiders.add_argument("--filings", type=int, default=10)
    sec_insiders.add_argument("--include-amendments", action="store_true")
    sec_13f = sub.add_parser("sec-13f", help="Fetch delayed SEC 13F institutional holdings (requires SEC_USER_AGENT)")
    sec_13f.add_argument("manager_ticker")
    sec_earnings = sub.add_parser("sec-earnings", help="Fetch official reported earnings dates from SEC 8-K Item 2.02")
    sec_earnings.add_argument("ticker")
    sec_earnings.add_argument("--filings", type=int, default=20)
    treasury = sub.add_parser("treasury-debt", help="Fetch public U.S. Treasury daily debt data")
    treasury.add_argument("--start", help="Start date YYYY-MM-DD")
    treasury.add_argument("--limit", type=int, default=100)
    risk = sub.add_parser("risk", help="Calculate historical portfolio risk from aligned price history")
    risk.add_argument("tickers", help="Comma-separated ticker symbols")
    risk.add_argument("--weights", help="Comma-separated TICKER=WEIGHT pairs; defaults to equal weights")
    risk.add_argument("--range", dest="range_", default="5y", choices=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])
    risk.add_argument("--risk-free-rate", type=float, default=0.0, help="Annual risk-free rate as decimal, e.g. 0.03")
    backtest = sub.add_parser("backtest", help="Run a price-only periodic-rebalance historical baseline")
    backtest.add_argument("tickers", help="Comma-separated ticker symbols")
    backtest.add_argument("--weights", help="Comma-separated TICKER=WEIGHT pairs; defaults to equal weights")
    backtest.add_argument("--range", dest="range_", default="5y", choices=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])
    backtest.add_argument("--cash", type=float, default=10000.0)
    backtest.add_argument("--fee-bps", type=float, default=5.0)
    backtest.add_argument("--slippage-bps", type=float, default=5.0)
    backtest.add_argument("--rebalance-days", type=int, default=21)
    args = parser.parse_args()
    try:
        if args.command == "analyze":
            payload = analyze_stock(args.ticker)
            if args.macro:
                payload["macro_context"] = macro_snapshot(country=args.macro_country, currency=args.macro_currency)
        elif args.command == "quote":
            raw = quote_and_history(args.ticker)
            payload = {"market": {k: v for k, v in raw.items() if k not in {"history", "dividends"}},
                       "technical": analyze_history(raw["history"])}
        elif args.command == "compare":
            symbols = [x.strip().upper() for x in args.tickers.split(",") if x.strip()]
            if not symbols: raise ValueError("Provide at least one ticker")
            payload = {"comparisons": [analyze_stock(symbol) for symbol in symbols]}
        elif args.command == "portfolio": payload = analyze_portfolio(args.csv_path)
        elif args.command == "etf":
            metadata = json.loads(args.metadata_json.read_text(encoding="utf-8"))
            if args.verify_fsma:
                metadata["fsma_registry"] = fetch_fsma_uci_registry(isin=metadata.get("isin"), name=metadata.get("fund_name"))
            payload = analyze_etf(metadata)
        elif args.command == "fsma-uci":
            payload = fetch_fsma_uci_registry(isin=args.isin, name=args.name, limit=args.limit)
        elif args.command == "be-tob":
            payload = calculate_tob(args.amount, legal_form=args.legal_form, distribution=args.distribution,
                                    registration=args.registration, side=args.side)
        elif args.command == "be-net-dividend":
            payload = calculate_net_dividend_yield(
                annual_distribution_per_share=args.distribution_per_share, market_price=args.price,
                shares=args.shares, legal_form=args.legal_form, fcp_breakdown_available=args.fcp_breakdown,
                belgian_withholding_rate_pct=args.belgian_withholding,
                investor_level_foreign_withholding_pct=args.foreign_withholding,
            )
        elif args.command == "ecb-fx":
            payload = {"observations": euro_reference_rates(args.currency, start=args.start, end=args.end)}
        elif args.command == "eurostat":
            filters = {}
            for item in args.filter:
                if "=" not in item: raise ValueError(f"Invalid filter {item!r}; use DIM=VALUE")
                key, value = item.split("=", 1); filters[key] = value
            payload = {"observations": fetch_dataset(args.dataset, filters=filters)}
        elif args.command == "nbb": payload = {"observations": fetch_sdmx_csv(args.url)}
        elif args.command == "nbb-preset":
            payload = {"presets": list_nbb_presets()} if not args.name else {"observations": fetch_nbb_preset(args.name, start_period=args.start_period)}
        elif args.command == "worldbank":
            payload = {"observations": fetch_indicator(args.country, args.indicator, start=args.start, end=args.end)}
        elif args.command == "macro": payload = macro_snapshot(country=args.country, currency=args.currency)
        elif args.command == "cftc-cot":
            rows = fetch_legacy_futures_only(commodity=args.commodity, start_date=args.start, limit=args.limit)
            payload = {"observations": rows, "summary": positioning_summary(rows) if rows else {"status": "unavailable"}}
        elif args.command == "fred":
            payload = {"observations": fetch_fred_series(args.series_id, start=args.start, end=args.end),
                       "notice": "This product uses the FRED API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.",
                       "terms_url": "https://fred.stlouisfed.org/legal/terms/"}
        elif args.command == "sec-insiders":
            rows = fetch_form4_transactions(args.ticker, limit_filings=args.filings, include_amendments=args.include_amendments)
            payload = {"transactions": rows, "sentiment": insider_sentiment(rows),
                       "notice": "Form 4 filings are source disclosures; review transaction codes, indirect ownership, amendments and 10b5-1 plans."}
        elif args.command == "sec-13f":
            rows = fetch_13f_holdings(args.manager_ticker)
            payload = {"holdings": rows,
                       "notice": "13F reports are delayed long-equity disclosures; they are not complete real-time portfolios and omit short positions."}
        elif args.command == "sec-earnings":
            rows = fetch_reported_earnings_filings(args.ticker, limit_filings=args.filings)
            payload = {"events": rows,
                       "notice": "Official reported dates only: SEC 8-K Item 2.02. Not a forward calendar, no consensus/EPS estimates; foreign private issuers using 6-K are not included."}
        elif args.command == "treasury-debt":
            payload = {"observations": fetch_debt_to_penny(start_date=args.start, limit=args.limit)}
        elif args.command in {"risk", "backtest"}:
            symbols = [value.strip().upper() for value in args.tickers.split(",") if value.strip()]
            if not symbols:
                raise ValueError("Provide at least one ticker.")
            weights = None
            if args.weights:
                weights = {}
                for item in args.weights.split(","):
                    if "=" not in item:
                        raise ValueError(f"Invalid weight {item!r}; use TICKER=WEIGHT")
                    symbol, value = item.split("=", 1)
                    weights[symbol.strip().upper()] = float(value)
            if args.command == "risk":
                if not 0 <= args.risk_free_rate < 1:
                    raise ValueError("--risk-free-rate must be between 0 and 1.")
                payload = analyze_live_portfolio_risk(symbols, weights, range_=args.range_, risk_free_rate=args.risk_free_rate)
            else:
                payload = run_historical_backtest(
                    symbols, weights, range_=args.range_, initial_cash=args.cash,
                    fee_bps=args.fee_bps, slippage_bps=args.slippage_bps,
                    rebalance_every=args.rebalance_days,
                )
        print(json.dumps(payload, indent=2, ensure_ascii=False)); return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
