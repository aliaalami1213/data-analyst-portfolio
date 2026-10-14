# Data

All figures are in **millions of yen** unless stated. Fiscal years follow Sony's convention: **FY2025 = the year ended March 31, 2026**.

| File | Contents | Source |
|---|---|---|
| `income_statement.csv` | Consolidated statements of income, FY2023–FY2025, plus depreciation and amortization | [Sony Group Form 20-F for FY2025](https://www.sec.gov/Archives/edgar/data/313838/000119312526274893/d28719d20f.htm) (SEC EDGAR, filed 2026-06-18) |
| `balance_sheet.csv` | Consolidated statements of financial position, March 31, 2025 and 2026 | Same filing |
| `cash_flow.csv` | Selected lines from the consolidated statements of cash flows, FY2023–FY2025 | Same filing |
| `segment_sales.csv` | Total sales by segment, FY2021–FY2025 | Segment notes of the FY2025 filing and the [FY2023 filing](https://www.sec.gov/Archives/edgar/data/313838/000119312524167500/) (for FY2021–FY2022) |
| `market_inputs.csv` | Share price, exchange rate, bond yield, share count, tax rates | Sources listed per row in the file |
| `revenue_forecast.csv` | Output of `forecast_revenue.py` — starting growth rate per segment | Generated |

**Financial Services.** Sony spun off its Financial Services business in FY2025, so the FY2025 filing presents it as a discontinued operation and restates FY2023–FY2024 income and cash flows to exclude it. The March 31, 2025 balance sheet still carries the Financial Services assets and liabilities, so it is not comparable with March 31, 2026.

The values were transcribed from the filing's XBRL financial statement tables (pages `R2`, `R4`, `R7`, `R74`–`R76` of the filing's interactive data), not from a Kaggle dataset: Sony's own SEC filing is the primary source.
