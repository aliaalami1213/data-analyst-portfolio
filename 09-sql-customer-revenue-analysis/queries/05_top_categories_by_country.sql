-- Top 3 first-choice product categories in each of the 5 largest markets,
-- by revenue of the customers who prefer them (join + top-N-per-group).
WITH top_markets AS (
    SELECT country
    FROM customers
    GROUP BY country
    ORDER BY SUM(total_spent_usd) DESC
    LIMIT 5
),
category_revenue AS (
    SELECT
        c.country,
        cc.category,
        COUNT(*)               AS customers,
        SUM(c.total_spent_usd) AS revenue_usd
    FROM customers c
    JOIN customer_categories cc
      ON cc.customer_id = c.customer_id
     AND cc.preference_rank = 1
    WHERE c.country IN (SELECT country FROM top_markets)
    GROUP BY c.country, cc.category
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY revenue_usd DESC) AS category_rank,
        100.0 * revenue_usd / SUM(revenue_usd) OVER (PARTITION BY country) AS pct_of_country_revenue
    FROM category_revenue
)
SELECT
    country,
    category_rank,
    category,
    customers,
    ROUND(revenue_usd)               AS revenue_usd,
    ROUND(pct_of_country_revenue, 1) AS pct_of_country_revenue
FROM ranked
WHERE category_rank <= 3
ORDER BY country, category_rank;
