-- Does retention improve with tenure? Group customers into acquisition cohorts
-- (by years since first purchase) and compare each cohort to the previous one.
WITH cohorts AS (
    SELECT
        CASE
            WHEN tenure_months < 12 THEN '0: under 1 yr'
            WHEN tenure_months < 24 THEN '1: 1-2 yrs'
            WHEN tenure_months < 36 THEN '2: 2-3 yrs'
            WHEN tenure_months < 60 THEN '3: 3-5 yrs'
            ELSE                         '4: 5+ yrs'
        END AS tenure_cohort,
        is_churned,
        total_spent_usd,
        tenure_months
    FROM customers
),
summary AS (
    SELECT
        tenure_cohort,
        COUNT(*)                                             AS customers,
        100.0 * AVG(1 - is_churned)                          AS active_rate_pct,
        AVG(total_spent_usd)                                 AS avg_spend_usd,
        SUM(total_spent_usd) / SUM(tenure_months)            AS spend_per_tenure_month_usd
    FROM cohorts
    GROUP BY tenure_cohort
)
SELECT
    tenure_cohort,
    customers,
    ROUND(active_rate_pct, 1)                                             AS active_rate_pct,
    ROUND(active_rate_pct - LAG(active_rate_pct) OVER (ORDER BY tenure_cohort), 1)
                                                                          AS pp_change_vs_prev_cohort,
    ROUND(avg_spend_usd)                                                  AS avg_spend_usd,
    ROUND(spend_per_tenure_month_usd)                                     AS spend_per_tenure_month_usd
FROM summary
ORDER BY tenure_cohort;
