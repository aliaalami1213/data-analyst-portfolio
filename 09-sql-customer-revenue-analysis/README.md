# Customer Revenue & Retention Analysis in SQL

**Dataset:** the same [E-Commerce Customer Segmentation 2026 (Kaggle)](https://www.kaggle.com/datasets/datascikhan/e-commerce-customer-segmentation-2026) file used in [project 4](../04-ecommerce-customer-segmentation) — 50,000 customers — loaded into SQLite and analyzed entirely in SQL.

## Business Question
Where does revenue actually come from, which customers are worth winning back, and do tenure, channel, or category explain any of it? Project 4 answered this with Python models; this project answers the reporting-side version with the SQL an analyst would write against a warehouse.

## Approach
1. **Model the data** ([`schema.sql`](./schema.sql)) — load the flat 53-column CSV into a staging table, then build a clean `customers` table (raw fields only — the file's pre-computed labels are dropped so every metric is derived in SQL) and unpivot the three `preferred_category_*` columns into a `customer_categories` table.
2. **Check data quality** before trusting any number.
3. **Answer five business questions**, one query file each.

| Query | Question | SQL techniques |
|---|---|---|
| [`01_data_quality_checks`](./queries/01_data_quality_checks.sql) | Can the data be trusted? | `UNION ALL`, conditional aggregation, `NOT EXISTS` |
| [`02_revenue_concentration`](./queries/02_revenue_concentration.sql) | How concentrated is revenue? | CTEs, `NTILE`, running total with `SUM() OVER` |
| [`03_tenure_cohort_retention`](./queries/03_tenure_cohort_retention.sql) | Does retention improve with tenure? | `CASE` cohorts, `LAG` |
| [`04_channel_unit_economics`](./queries/04_channel_unit_economics.sql) | Which channels pay back? | `RANK`, comparison to window average |
| [`05_top_categories_by_country`](./queries/05_top_categories_by_country.sql) | What sells in the biggest markets? | `JOIN`, subquery, `ROW_NUMBER ... PARTITION BY` (top-N per group) |
| [`06_revenue_at_risk`](./queries/06_revenue_at_risk.sql) | Who should retention call first? | `PERCENT_RANK ... PARTITION BY`, window over aggregate |

## Key Findings
- **Revenue is concentrated: the top 20% of customers generate 48.9% of the $2.51B total, and the top 30% generate 64.2%.** The bottom 30% contribute under 5%.

  | Spend decile | Min. spend | % of revenue | Cumulative % | Churn rate |
  |---|---|---|---|---|
  | 1 (top 10%) | $117,919 | 28.7% | 28.7% | 30.8% |
  | 2 | $88,197 | 20.2% | 48.9% | 29.8% |
  | 3 | $66,932 | 15.3% | 64.2% | 29.9% |
  | 4–10 | — | 35.8% | 100% | 30.1–31.6% |

- **Churn does not depend on value.** Every spend decile churns at 30–32% — the best customers lapse as often as the worst, so losses at the top are disproportionately expensive.
- **$222M of lifetime revenue sits with 1,541 lapsed high-value customers** (top 10% of spend in their own country, inactive 60+ days). **534 of them lapsed only 61–90 days ago** and account for 34.8% of that revenue — the natural first win-back list.
- **Tenure buys no loyalty here.** The active rate is 69.4–70.6% in every tenure cohort, from under 1 year to 5+ years, and average lifetime spend is flat at ~$50k regardless of tenure.
- **Channels are interchangeable on unit economics.** Mobile App ranks first on LTV:CAC and In-Store last, but the spread is under 2% (495× vs. 486×), with churn within one point (29.7–30.7%) — not a difference to reallocate budget on.
- **No market has a dominant category.** Across the five largest markets the top first-choice category holds only 8.9–9.8% of revenue out of 12 categories, close to an even split.
- **Data quality:** `customer_id` is unique, total spend reconciles to purchases × average order value for every row, and 262 customers have zero spend (kept, and they land in the bottom decile).

## Recommendations
1. **Segment retention by value, not by tenure, channel, or category** — value is the only dimension in this data where customers differ meaningfully.
2. **Start win-back with the 534 high-value customers who lapsed 61–90 days ago** before working older lapsed accounts.
3. **Don't shift acquisition budget between channels on this evidence** — the LTV:CAC gap is inside noise.

## Limitations
This is a synthetic Kaggle dataset, and the flat results for tenure, channel, and category look like independently generated columns rather than real customer behavior (project 4 reached the same conclusion from the modeling side). It is also a customer-level snapshot with no order table, so true month-by-month cohort retention can't be computed; tenure cohorts are the closest available proxy. Revenue "at risk" is historical lifetime spend, not a forecast.

## Run it
```bash
python build_db.py
```
Builds `ecommerce.db` from project 4's CSV, runs every query, and writes each result to `results/`. Requires only `pandas` (SQLite ships with Python).

## Files
- `schema.sql` — staging → `customers` and `customer_categories` tables
- `queries/` — one `.sql` file per business question
- `results/` — query outputs as CSV
- `build_db.py` — loads the CSV and runs everything
