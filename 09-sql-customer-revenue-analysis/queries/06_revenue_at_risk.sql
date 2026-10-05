-- Win-back sizing: churned customers whose spend is in the top 10% of their own
-- country, bucketed by how long they have been inactive. The most recently lapsed
-- bucket is the list a retention team would work first.
WITH scored AS (
    SELECT
        customer_id,
        country,
        total_spent_usd,
        days_since_last_purchase,
        is_churned,
        PERCENT_RANK() OVER (PARTITION BY country ORDER BY total_spent_usd) AS spend_pctile_in_country
    FROM customers
),
lapsed_high_value AS (
    SELECT
        *,
        CASE
            WHEN days_since_last_purchase <= 90  THEN '1: 61-90 days'
            WHEN days_since_last_purchase <= 180 THEN '2: 91-180 days'
            WHEN days_since_last_purchase <= 365 THEN '3: 181-365 days'
            ELSE                                      '4: over 1 year'
        END AS inactivity_bucket
    FROM scored
    WHERE spend_pctile_in_country >= 0.90
      AND is_churned
)
SELECT
    inactivity_bucket,
    COUNT(*)                                                   AS customers,
    COUNT(DISTINCT country)                                    AS countries,
    ROUND(SUM(total_spent_usd))                                AS lifetime_revenue_usd,
    ROUND(AVG(total_spent_usd))                                AS avg_lifetime_spend_usd,
    ROUND(100.0 * SUM(total_spent_usd) / SUM(SUM(total_spent_usd)) OVER (), 1)
                                                               AS pct_of_revenue_at_risk,
    ROUND(100.0 * SUM(SUM(total_spent_usd)) OVER (ORDER BY inactivity_bucket)
                / SUM(SUM(total_spent_usd)) OVER (), 1)        AS cumulative_pct
FROM lapsed_high_value
GROUP BY inactivity_bucket
ORDER BY inactivity_bucket;
