#!/usr/bin/env python3
"""Stock Intelligence Engine CLI entrypoint."""
__version__ = "2.57.0"

from sie.analyzer import run_report
from sie.config import load_config
import argparse
import inspect

def main():
    parser = argparse.ArgumentParser(description=f"Stock Intelligence Engine v{__version__}", allow_abbrev=False)
    parser.add_argument("--backtest", action="store_true", help="Run backtest on watchlist")
    parser.add_argument("--portfolio", action="store_true", help="Show portfolio correlation & risk metrics")
    parser.add_argument("--news", action="store_true", help="Include news headlines")
    parser.add_argument("--export", action="store_true", help="Export CSV")
    parser.add_argument("--alerts", action="store_true", help="Force multi-channel alert router evaluation & send")
    parser.add_argument("--telegram", action="store_true", help="Enable Telegram channel for this run")
    parser.add_argument("--no-thesis", action="store_true", help="Disable thesis generation")
    parser.add_argument("--no-brief", action="store_true", help="Disable self-explaining signal brief")
    parser.add_argument("--no-honesty", action="store_true", help="Disable honesty / contradiction detector")
    parser.add_argument("--no-confidence", action="store_true", help="Disable signal confidence calibration & self-critique")
    parser.add_argument("--no-regime", action="store_true", help="Disable market regime adaptive overlay weighting")
    parser.add_argument("--no-supply-chain", action="store_true", help="Disable semiconductor / AI supply-chain CapEx tracker")
    parser.add_argument("--no-short-interest", action="store_true", help="Disable FINRA short volume / short interest overlay")
    parser.add_argument("--no-attention", action="store_true", help="Disable Wikipedia / search attention momentum tracker")
    parser.add_argument("--no-authenticity", action="store_true", help="Disable authenticity-filtered social narrative velocity overlay")
    parser.add_argument("--no-social-intent", action="store_true", help="Disable social trading action intent classifier")
    parser.add_argument("--no-credit-spread", action="store_true", help="Disable corporate credit spread / CDS momentum overlay")
    parser.add_argument("--no-earnings-call", action="store_true", help="Disable earnings-call transcript sentiment & guidance drift overlay")
    parser.add_argument("--no-news-authority", action="store_true", help="Disable news-source authority / reliability weighted narrative overlay")
    parser.add_argument("--no-whisper-number", action="store_true", help="Disable whisper number / pre-earnings alt-data beat probability overlay")
    parser.add_argument("--no-kol-amplification", action="store_true", help="Disable KOL / influencer narrative amplification detector")
    parser.add_argument("--no-etf-flow", action="store_true", help="Disable ETF creation/redemption & AP flow overlay")
    parser.add_argument("--no-buyback-10b51", action="store_true", help="Disable Rule 10b5-1 / buyback authorization vs execution overlay")
    parser.add_argument("--no-employee-outlook", action="store_true", help="Disable employee outlook / Glassdoor business sentiment overlay")
    parser.add_argument("--no-unusual-options", action="store_true", help="Disable unusual options sweep vs block confirmation overlay")
    parser.add_argument("--no-consumer-spend", action="store_true", help="Disable aggregated consumer transaction / credit-card panel spend nowcasting overlay")
    parser.add_argument("--no-borrow-fee", action="store_true", help="Disable securities lending / borrow fee & short squeeze risk overlay")
    parser.add_argument("--no-contagion", action="store_true", help="Disable cross-ticker narrative contagion detector")
    parser.add_argument("--no-estimate-revision", action="store_true", help="Disable analyst estimate revision velocity & breadth overlay")
    parser.add_argument("--no-patent-momentum", action="store_true", help="Disable patent & intellectual property filing momentum overlay")
    parser.add_argument("--no-digital-footprint", action="store_true", help="Disable company digital footprint momentum overlay (web traffic + app downloads)")
    parser.add_argument("--no-gex", action="store_true", help="Disable dealer gamma exposure (GEX) & pin-risk overlay")
    parser.add_argument("--no-app-store-reviews", action="store_true", help="Disable app-store review sentiment & complaint velocity overlay")
    parser.add_argument("--no-retail-flow", action="store_true", help="Disable retail brokerage order-flow imbalance overlay")
    parser.add_argument("--no-hiring-skill-mix", action="store_true", help="Disable job-posting skill-mix & posted-compensation inflation overlay")
    parser.add_argument("--no-tokenized-basis", action="store_true", help="Disable cross-venue tokenized-share basis / on-chain equity premium overlay")
    parser.add_argument("--no-news-materiality", action="store_true", help="Disable news materiality / predicted next-session impact overlay")
    parser.add_argument("--no-dilution-atm", action="store_true", help="Disable secondary offering / ATM dilution velocity overlay")
    parser.add_argument("--no-trace-flow", action="store_true", help="Disable TRACE corporate-bond customer-flow and liquidity shock overlay")
    parser.add_argument("--no-primary-credit", action="store_true", help="Disable primary credit issuance concession and supply-pressure overlay")
    parser.add_argument("--no-target-stance", action="store_true", help="Disable target-specific financial stance and narrative specificity overlay")
    parser.add_argument("--no-alt-data-provenance", action="store_true", help="Disable alternative-data provenance and AI-synthetic contamination overlay")
    parser.add_argument("--no-rule-606", action="store_true", help="Disable Rule 606 retail options routing and execution-quality overlay")
    parser.add_argument("--no-index-reconstitution", action="store_true", help="Disable index reconstitution and forced passive-flow overlay")
    parser.add_argument("--no-earnings-event-contract", action="store_true", help="Disable listed earnings event-contract vs whisper overlay")
    args = parser.parse_args()
    kwargs = dict(
        include_news=args.news or True,
        export=args.export,
        backtest=args.backtest,
        telegram=args.telegram or args.alerts,
        include_thesis=not args.no_thesis,
        include_brief=not args.no_brief,
        include_honesty=not args.no_honesty,
        include_confidence=not args.no_confidence,
        include_regime=not args.no_regime,
        include_supply_chain=not args.no_supply_chain,
        include_short_interest=not args.no_short_interest,
        include_attention=not args.no_attention,
        include_authenticity=not args.no_authenticity,
        include_social_intent=not args.no_social_intent,
        include_credit_spread=not args.no_credit_spread,
        include_earnings_call=not args.no_earnings_call,
        include_news_authority=not args.no_news_authority,
        include_whisper_number=not args.no_whisper_number,
        include_kol_amplification=not args.no_kol_amplification,
        include_etf_flow=not args.no_etf_flow,
        include_buyback_10b51=not args.no_buyback_10b51,
        include_employee_outlook=not args.no_employee_outlook,
        include_unusual_options=not args.no_unusual_options,
        include_consumer_spend=not args.no_consumer_spend,
        include_borrow_fee=not args.no_borrow_fee,
        include_contagion=not args.no_contagion,
        include_estimate_revision=not args.no_estimate_revision,
        include_patent_momentum=not args.no_patent_momentum,
        include_digital_footprint=not args.no_digital_footprint,
        include_gex=not args.no_gex,
        include_app_store_reviews=not args.no_app_store_reviews,
        include_retail_flow=not args.no_retail_flow,
        include_hiring_skill_mix=not args.no_hiring_skill_mix,
        include_tokenized_basis=not args.no_tokenized_basis,
        include_news_materiality=not args.no_news_materiality,
        include_dilution_atm=not args.no_dilution_atm,
        include_trace_flow=not args.no_trace_flow,
        include_primary_credit=not args.no_primary_credit,
        include_target_stance=not args.no_target_stance,
        include_alt_data_provenance=not args.no_alt_data_provenance,
        include_rule_606=not args.no_rule_606,
        include_index_reconstitution=not args.no_index_reconstitution,
        include_earnings_event_contract=not args.no_earnings_event_contract,
    )
    parameters = inspect.signature(run_report).parameters
    accepts_var_kwargs = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )
    forwarded = kwargs if accepts_var_kwargs else {
        key: value for key, value in kwargs.items() if key in parameters
    }
    run_report(**forwarded)

    if not args.no_unusual_options:
        from sie.unusual_options import detect_unusual_options
        sample = detect_unusual_options("NVDA")
        print(f"UOPT overlay ready source={sample.get('source')} boost={sample.get('signal_boost')}")

    if not args.no_employee_outlook:
        from sie.employee_outlook import detect_employee_outlook
        sample = detect_employee_outlook("NVDA")
        print(f"EO overlay ready source={sample.get('source')} boost={sample.get('signal_boost')}")

    if not args.no_app_store_reviews:
        from sie.app_store_reviews import detect_app_store_reviews
        sample = detect_app_store_reviews("AAPL")
        print(f"ASR overlay ready source={sample.get('source')} boost={sample.get('signal_boost')}")

    if not args.no_retail_flow:
        from sie.retail_flow import detect_retail_flow
        sample = detect_retail_flow("NVDA")
        print(f"RFLOW overlay ready source={sample.get('source')} boost={sample.get('signal_boost')}")

    if not args.no_hiring_skill_mix:
        from sie.hiring_skill_mix import detect_hiring_skill_mix
        sample = detect_hiring_skill_mix("NVDA")
        print(f"HMIX overlay ready source={sample.get('source')} boost={sample.get('signal_boost')}")

    if not args.no_tokenized_basis:
        from sie.tokenized_basis import detect_tokenized_basis
        sample = detect_tokenized_basis("NVDA")
        print(f"TOK overlay ready source={sample.get('source')} boost={sample.get('signal_boost')}")

    if not args.no_news_materiality:
        from sie.news_materiality import detect_news_materiality
        sample = detect_news_materiality("NVDA")
        print(f"NIMP overlay ready source={sample.get('source')} boost={sample.get('signal_boost')} bucket={sample.get('nimp_vol_bucket')}")

    if not args.no_dilution_atm:
        from sie.dilution_atm import detect_dilution_atm
        sample = detect_dilution_atm("PLTR")
        print(f"DIL overlay ready source={sample.get('source')} vel={sample.get('dil_atm_velocity')} delta={sample.get('dil_share_delta')} boost={sample.get('signal_boost')}")

    if not args.no_trace_flow:
        from sie.trace_flow import detect_trace_flow
        sample = detect_trace_flow("JPM")
        print(f"TRACE overlay ready source={sample.get('source')} flow={sample.get('trace_customer_flow')} liq={sample.get('trace_liq_score')} boost={sample.get('signal_boost')}")

    if not args.no_primary_credit:
        from sie.primary_credit import detect_primary_credit
        sample = detect_primary_credit("AAPL")
        print(f"PCI overlay ready source={sample.get('source')} concession={sample.get('pci_concession_bp')} supply={sample.get('pci_supply_score')} boost={sample.get('signal_boost')}")

    if not args.no_target_stance:
        from sie.target_stance import detect_target_stance
        sample = detect_target_stance("NVDA")
        print(f"TSN overlay ready source={sample.get('source')} stance={sample.get('tsn_stance')} spec={sample.get('tsn_specificity')} gap={sample.get('tsn_qa_gap')} boost={sample.get('signal_boost')}")

    if not args.no_alt_data_provenance:
        from sie.alt_data_provenance import detect_alt_data_provenance
        sample = detect_alt_data_provenance("NVDA")
        print(f"ADP overlay ready source={sample.get('source')} provenance={sample.get('adp_provenance')} cross={sample.get('adp_crosscheck')} boost={sample.get('signal_boost')}")

    if not args.no_rule_606:
        from sie.rule_606 import detect_rule_606
        sample = detect_rule_606("NVDA")
        print(f"R606 overlay ready source={sample.get('source')} concentration={sample.get('r606_concentration')} exec={sample.get('r606_exec_quality')} boost={sample.get('signal_boost')}")
    if not args.no_index_reconstitution:
        from sie.index_reconstitution import detect_index_reconstitution
        sample = detect_index_reconstitution("PLTR")
        print(f"IDX overlay ready source={sample.get('source')} event={sample.get('idx_event')} forced_usd={sample.get('idx_forced_usd')} boost={sample.get('signal_boost')}")
    if not args.no_earnings_event_contract:
        from sie.earnings_event_contract import detect_earnings_event_contract
        sample = detect_earnings_event_contract("NVDA")
        print(f"EEC overlay ready source={sample.get('source')} implied={sample.get('eec_implied_beat')} gap={sample.get('eec_whisper_gap')} boost={sample.get('signal_boost')}")

if __name__ == "__main__":
    main()
