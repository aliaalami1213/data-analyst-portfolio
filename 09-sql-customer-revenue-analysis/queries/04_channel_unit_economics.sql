-- Which acquisition channels pay back? Revenue per customer vs. acquisition cost,
-- with each channel ranked on LTV:CAC and compared to the all-channel average.
WITH channel AS (
    SELECT
        shopping_channel,
        COUNT(*)                                   AS customers,
        AVG(total_spent_usd)                       AS avg_revenue_usd,
        AVG(cac_usd)                               AS avg_cac_usd,
        SUM(total_spent_usd) / SUM(cac_usd)        AS ltv_to_cac,
        AVG(is_churned)                            AS churn_rate,
        1.0 * SUM(return_count) / SUM(total_purchases) AS return_rate
    FROM customers
    GROUP BY shopping_channel
)
SELECT
    shopping_channel,
    customers,
    ROUND(avg_revenue_usd)                                         AS avg_revenue_usd,
    ROUND(avg_cac_usd, 2)                                          AS avg_cac_usd,
    ROUND(ltv_to_cac)                                              AS ltv_to_cac,
    RANK() OVER (ORDER BY ltv_to_cac DESC)                         AS ltv_to_cac_rank,
    ROUND(100.0 * (avg_revenue_usd / AVG(avg_revenue_usd) OVER () - 1), 1)
                                                                   AS revenue_vs_avg_pct,
    ROUND(100.0 * churn_rate, 1)                                   AS churn_rate_pct,
    ROUND(100.0 * return_rate, 1)                                  AS return_rate_pct
FROM channel
ORDER BY ltv_to_cac_rank;
