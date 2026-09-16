# Sony (SONY) Stock — Technical Analysis, Volatility & Backtesting

**Dataset:** [Sony Stock Data (Kaggle)](https://www.kaggle.com/datasets/nilesh2042/sony-stock-data) — daily OHLCV for Sony (NYSE: SONY), 2014-01-02 to 2026-08-24 (3,179 trading days)

## Business Question
What does 12+ years of Sony's daily price history say about its trend, momentum, and risk — and do standard technical-indicator strategies or time-series models actually add value over simply buying and holding?

## Approach
1. **Clean & overview** — check for missing/duplicate data, plot price and volume history, compute total return/CAGR.
2. **Moving averages** — SMA(20/50/200) and EMA(20) to read the underlying trend.
3. **Momentum indicators** — RSI(14) and MACD(12,26,9).
4. **Bollinger Bands** — 20-day SMA ± 2σ to read volatility-relative price extension.
5. **Volatility analysis** — daily returns, 30-day rolling annualized volatility, and volatility by year across macro cycles (COVID 2020, 2022 rate hikes).
6. **Time series forecasting** — ARIMA(5,1,0) on a 60-day holdout, tested both as a multi-step forecast and a fairer one-step walk-forward forecast, each compared against naive baselines.
7. **Backtesting** — a SMA(20/50) crossover strategy vs. buy & hold, with CAGR, volatility, Sharpe ratio, and max drawdown.

## Key Findings
- Sony returned **657% total (17.4% CAGR)** from Jan 2014 to Aug 2026, but with **30% annualized volatility** and a **-50.6% max drawdown** (around Oct 2022) — high return, high risk, not a smooth ride.
- Yearly volatility ranged from **22.7% (2017) to 36.5% (2016)**, with visible spikes in **2020** (COVID) and **2022** (rate-hiking cycle) — risk is regime-dependent, which matters for position sizing.
- **ARIMA adds no measurable edge over a naive random-walk forecast.** At a 60-day horizon its forecast ties a flat-price baseline (RMSE 1.36 vs. 1.36); even a fairer one-step walk-forward test ties "tomorrow's price = today's price" almost exactly (RMSE 0.443 vs. 0.443, MAPE 1.62% vs. 1.63%). Daily prices behave close enough to a random walk that classic time-series models don't earn their keep here.
- A **SMA(20/50) crossover strategy trades return for risk, not for free performance**: -4.6pp CAGR (12.8% vs. 17.4%) but ~8.5pp less volatility and ~17pp shallower drawdowns than buy & hold, landing at essentially the same Sharpe ratio (0.67 vs. 0.68) — and that comparison still ignores transaction costs across 59 trades.
- As of the last observation, the technical picture is **moderately bullish and non-overbought**: RSI(14) ≈ 65, MACD above its signal line, price above both the 50- and 200-day SMA.

## Recommendations
1. Don't rely on ARIMA (or similar univariate time-series models) for daily price *direction* forecasts on this stock — treat it close to a random walk. Forecasting improvements would need external signals (earnings, macro, options-implied volatility), not price history alone.
2. Size positions and set risk limits using the **regime-aware volatility view**, not one blanket volatility number — 2020/2022-style spikes can more than double typical risk.
3. Frame a trend-following rule like SMA crossover as a **risk-management tool** (smoother ride, shallower drawdowns), not a return-enhancer — and factor in transaction costs before using it live.
4. Treat RSI/MACD/Bollinger readings as **context for entries/exits** around a thesis formed elsewhere, not as standalone predictive signals.

Full code and outputs are in [`analysis.ipynb`](./analysis.ipynb).

## Files
- `analysis.ipynb` — full notebook: cleaning → technical indicators → volatility → ARIMA forecasting → backtesting → findings & recommendations
- `data/` — the dataset CSV (included directly, no download needed) + `data/README.md` with the source link
- `images/` — exported charts referenced above and in the notebook
