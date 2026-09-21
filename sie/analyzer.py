"""Orchestrate narrative + technical analysis including Dealer Gamma Exposure (GEX) & Pin-Risk Overlay."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sie.config import load_config
from sie.i18n import t, translate_reason
from sie.news import fetch_headlines
from sie.technical import analyze_ticker
from sie.social import integrate_social_to_row, forecast_narrative_phase
from sie.insider import integrate_insider_to_row
from sie.prediction_markets import integrate_prediction_markets_to_row
from sie.institutional import integrate_institutional_to_row
from sie.congressional import integrate_congressional_to_row
from sie.realtime import integrate_realtime_to_row
from sie.dark_pool import integrate_dark_pool_to_row
from sie.options_iv import integrate_options_iv_to_row
from sie.options_0dte import integrate_options_0dte_to_row
from sie.edgar import integrate_edgar_to_row
from sie.hiring import integrate_hiring_to_row
from sie.supply_chain import integrate_supply_chain_to_row
from sie.short_interest import integrate_short_interest_to_row
from sie.attention import integrate_attention_to_row
from sie.authenticity import integrate_authenticity_to_row
from sie.social_intent import integrate_social_intent_to_row
from sie.credit_spread import integrate_credit_spread_to_row
from sie.earnings_call import integrate_earnings_call_to_row
from sie.news_authority import integrate_news_authority_to_row
from sie.consumer_spend import integrate_consumer_spend_to_row
from sie.borrow_fee import integrate_borrow_fee_to_row
from sie.contagion import integrate_contagion_to_row
from sie.estimate_revision import integrate_estimate_revision_to_row
from sie.patent_momentum import integrate_patent_momentum_to_row
from sie.digital_footprint import integrate_digital_footprint_to_row
from sie.gex import integrate_gex_to_row
from sie.thesis import integrate_thesis_to_row
from sie.brief import integrate_brief_to_row
from sie.honesty import integrate_honesty_to_row
from sie.confidence import integrate_confidence_to_row
from sie.regime import integrate_regime_to_row
from sie.alerts import format_telegram_body, send_telegram_message
from sie.backtest import backtest_watchlist
