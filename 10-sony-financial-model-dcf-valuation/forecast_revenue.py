"""Step 1 of the model: forecast Sony's sales by segment for FY2026-FY2030.

Reads   data/segment_sales.csv   (five fiscal years of reported segment sales)
Writes  data/revenue_forecast.csv (starting growth rate per segment -> Excel model input)
        data/backtest_results.csv (hold-out accuracy of each candidate method)
        images/01_segment_sales_forecast.png

With only five annual observations per segment, a statistical time-series model
(ARIMA, ETS) cannot be fitted responsibly. Instead, three simple growth rules are
backtested on hold-out years, and the most accurate one sets each segment's
starting growth rate. Growth then fades linearly to a long-run rate by year five,
the standard treatment in a DCF so that no segment outgrows the economy forever.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
LONG_RUN_GROWTH = 0.02      # nominal long-run growth every segment fades to
GROWTH_CAP = (-0.05, 0.12)  # bounds on a segment's starting growth rate
HORIZON = 5

sales = pd.read_csv(HERE / "data" / "segment_sales.csv", index_col="segment")
years = [int(c[2:]) for c in sales.columns]


def naive(history):
    """Next year grows at last year's rate."""
    return history[-1] / history[-2] - 1


def cagr(history):
    """Next year grows at the compound average rate of the whole history."""
    return (history[-1] / history[0]) ** (1 / (len(history) - 1)) - 1


def linear_trend(history):
    """Next year continues the least-squares straight line through the history."""
    x = np.arange(len(history))
    slope, intercept = np.polyfit(x, history, 1)
    return (intercept + slope * len(history)) / history[-1] - 1


METHODS = {"Naive (last year's growth)": naive, "CAGR": cagr, "Linear trend": linear_trend}

# --- Backtest: predict FY2024 from FY2021-23, then FY2025 from FY2021-24 -------------
rows = []
for segment, history in sales.iterrows():
    values = history.to_numpy(dtype=float)
    for cutoff in (3, 4):
        actual = values[cutoff]
        for name, method in METHODS.items():
            predicted = values[cutoff - 1] * (1 + method(values[:cutoff]))
            rows.append({
                "segment": segment,
                "predicted_year": f"FY{years[cutoff]}",
                "method": name,
                "actual": actual,
                "predicted": round(predicted),
                "abs_pct_error": abs(predicted / actual - 1),
            })
backtest = pd.DataFrame(rows)
backtest.to_csv(HERE / "data" / "backtest_results.csv", index=False)

# Weight each segment's error by its size so large segments drive the choice.
weights = sales["FY2025"] / sales["FY2025"].sum()
backtest["weighted_error"] = backtest["abs_pct_error"] * backtest["segment"].map(weights)
by_method = backtest.groupby("method").agg(
    mape=("abs_pct_error", "mean"),
    sales_weighted_mape=("weighted_error", lambda e: e.sum() / 2),  # two hold-out years
).sort_values("sales_weighted_mape")
best_method = by_method.index[0]
print("Backtest accuracy (lower is better):")
print((by_method * 100).round(1).to_string())
print(f"\nSelected method: {best_method}")

# --- Forecast: starting growth from the selected method, faded to the long-run rate ---
forecast_years = [f"FY{years[-1] + i}" for i in range(1, HORIZON + 1)]
out = []
for segment, history in sales.iterrows():
    values = history.to_numpy(dtype=float)
    raw = METHODS[best_method](values)
    start = float(np.clip(raw, *GROWTH_CAP))
    growth = [start + (LONG_RUN_GROWTH - start) * i / (HORIZON - 1) for i in range(HORIZON)]
    level, path = values[-1], []
    for g in growth:
        level *= 1 + g
        path.append(round(level))
    out.append({"segment": segment, "method": best_method, "raw_growth": round(raw, 4),
                "start_growth": round(start, 4), **dict(zip(forecast_years, path))})
forecast = pd.DataFrame(out).set_index("segment")
forecast.to_csv(HERE / "data" / "revenue_forecast.csv")
print("\nStarting growth by segment:")
print((forecast[["raw_growth", "start_growth"]] * 100).round(1).to_string())

total_hist = sales.sum()
total_fcst = forecast[forecast_years].sum()
print(f"\nSegment sales FY{years[-1]}: {total_hist.iloc[-1] / 1e6:.2f}tn yen  ->  "
      f"{forecast_years[-1]}: {total_fcst.iloc[-1] / 1e6:.2f}tn yen "
      f"({(total_fcst.iloc[-1] / total_hist.iloc[-1]) ** (1 / HORIZON) - 1:.1%} CAGR)")

# --- Chart ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5))
labels = list(sales.columns) + forecast_years
main = [s for s in sales.index if s != "All Other"]
for segment, color in zip(main, plt.cm.tab10.colors):
    hist = sales.loc[segment] / 1e6
    fcst = forecast.loc[segment, forecast_years] / 1e6
    ax.plot(sales.columns, hist, marker="o", color=color, label=segment)
    ax.plot([sales.columns[-1]] + forecast_years, [hist.iloc[-1]] + list(fcst),
            marker="o", linestyle="--", color=color, markerfacecolor="white")
ax.axvline(len(sales.columns) - 1, color="grey", linewidth=0.8, linestyle=":")
ax.text(len(sales.columns) - 0.9, ax.get_ylim()[1] * 0.97, "forecast →", color="grey", va="top")
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels)
ax.set_ylabel("Segment sales (¥ trillion)")
ax.set_title("Sony segment sales: reported FY2021–FY2025 and base-case forecast")
ax.grid(axis="y", alpha=0.3)
ax.legend(frameon=False, fontsize=9)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "images" / "01_segment_sales_forecast.png", dpi=150)
