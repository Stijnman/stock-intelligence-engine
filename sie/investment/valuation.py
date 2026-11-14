"""Transparent scenario DCF."""
from typing import Any

def dcf_per_share(free_cash_flow: float, shares: float, net_cash: float = 0.0, growth: float = 0.08,
                  discount_rate: float = 0.09, terminal_growth: float = 0.025, years: int = 5) -> dict[str, Any]:
    if shares <= 0 or free_cash_flow <= 0: raise ValueError("DCF requires positive free cash flow and diluted shares")
    if discount_rate <= terminal_growth: raise ValueError("Discount rate must exceed terminal growth")
    projected = [free_cash_flow * (1 + growth) ** year for year in range(1, years + 1)]
    pv_cashflows = sum(value / (1 + discount_rate) ** year for year, value in enumerate(projected, 1))
    terminal = projected[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal / (1 + discount_rate) ** years
    equity = pv_cashflows + pv_terminal + net_cash
    return {"intrinsic_value_per_share": equity / shares, "enterprise_value": pv_cashflows + pv_terminal,
            "equity_value": equity, "projected_fcf": projected,
            "assumptions": {"starting_fcf": free_cash_flow, "shares": shares, "net_cash": net_cash,
                            "growth": growth, "discount_rate": discount_rate, "terminal_growth": terminal_growth, "years": years}}

def scenario_valuation(free_cash_flow: float, shares: float, net_cash: float = 0.0) -> dict[str, Any]:
    cases = {"bear": (0.03, 0.11, 0.015), "base": (0.08, 0.09, 0.025), "bull": (0.13, 0.085, 0.03)}
    return {name: dcf_per_share(free_cash_flow, shares, net_cash, growth=g, discount_rate=d, terminal_growth=t)
            for name, (g, d, t) in cases.items()}

def margin_of_safety(intrinsic_value: float, market_price: float) -> float | None:
    if intrinsic_value <= 0: return None
    return (1.0 - market_price / intrinsic_value) * 100.0
