-- How concentrated is revenue? Rank customers into spend deciles and
-- track the cumulative share of revenue (Pareto analysis).
WITH ranked AS (
    SELECT
        customer_id,
        total_spent_usd,
        is_churned,
        NTILE(10) OVER (ORDER BY total_spent_usd DESC) AS spend_decile
    FROM customers
),
by_decile AS (
    SELECT
        spend_decile,
        COUNT(*)             AS customers,
        MIN(total_spent_usd) AS min_spend_usd,
        SUM(total_spent_usd) AS revenue_usd,
        AVG(is_churned)      AS churn_rate
    FROM ranked
    GROUP BY spend_decile
)
SELECT
    spend_decile,
    customers,
    ROUND(min_spend_usd)                                              AS min_spend_usd,
    ROUND(revenue_usd)                                                AS revenue_usd,
    ROUND(100.0 * revenue_usd / SUM(revenue_usd) OVER (), 1)          AS pct_of_revenue,
    ROUND(100.0 * SUM(revenue_usd) OVER (ORDER BY spend_decile)
                / SUM(revenue_usd) OVER (), 1)                        AS cumulative_pct,
    ROUND(100.0 * churn_rate, 1)                                      AS churn_rate_pct
FROM by_decile
ORDER BY spend_decile;
