-- Before trusting any metric: row counts, key uniqueness, nulls, impossible values.
SELECT 'rows in customers'                 AS check_name, COUNT(*) AS value FROM customers
UNION ALL
SELECT 'distinct customer_id',             COUNT(DISTINCT customer_id) FROM customers
UNION ALL
SELECT 'null country',                     SUM(country IS NULL) FROM customers
UNION ALL
SELECT 'negative or zero spend',           SUM(total_spent_usd <= 0) FROM customers
UNION ALL
SELECT 'spend <> purchases x AOV (>1% off)',
       SUM(ABS(total_spent_usd - total_purchases * avg_order_value_usd) > 0.01 * total_spent_usd)
FROM customers
UNION ALL
SELECT 'customers with no category',
       (SELECT COUNT(*) FROM customers c
        WHERE NOT EXISTS (SELECT 1 FROM customer_categories cc WHERE cc.customer_id = c.customer_id))
UNION ALL
SELECT 'rows in customer_categories',      COUNT(*) FROM customer_categories;
