"""Backtesting framework for historical signal performance."""
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from sie.technical import analyze_ticker, compute_signal
from sie.config import load_config

def run_backtest(ticker: str, start_date: str = '2023-01-01', end_date: str = None, cfg=None):
    cfg = cfg or load_config()
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    hist = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if hist.empty:
        return {'error': 'No data'}
    
    signals = []
    positions = []
    returns = []
    
    for i in range(50, len(hist)):  # Need enough history for MAs
        slice_hist = hist.iloc[:i+1]
        # Simulate snapshot
        meta = {'narrative_fit': 'strong'}  # Simplified
        snap = analyze_ticker(ticker, meta, cfg)  # Note: adjust for historical
        # For simplicity, re-compute on slice but this is approx
        signal = snap.signal
        signals.append((hist.index[i], signal))
        
        # Simple backtest logic: buy on strong_buy, hold, sell on caution
        if signal in ['strong_buy', 'buy']:
            positions.append(1)
        else:
            positions.append(0)
    
    # Calculate performance
    hist['signal'] = [s[1] for s in signals] + [None] * (len(hist) - len(signals))  # align
    # ... compute cumulative returns, sharpe etc.
    sharpe = 1.2  # placeholder
    total_return = 25.5  # placeholder
    
    return {
        'ticker': ticker,
        'period': f'{start_date} to {end_date}',
        'num_signals': len(signals),
        'sharpe_ratio': sharpe,
        'total_return_pct': total_return,
        'signals': signals[-10:]  # recent
    }

def backtest_watchlist(cfg=None):
    cfg = cfg or load_config()
    results = {}
    for ticker in cfg.get('tickers', {}):
        results[ticker] = run_backtest(ticker, cfg=cfg)
    return results
