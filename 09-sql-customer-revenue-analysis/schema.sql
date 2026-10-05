-- Model the flat 53-column staging table into two analysis tables.

-- One row per customer: only the raw, non-derived fields.
-- The source file also ships pre-computed labels (rfm_category, clv_category, ...);
-- they are left behind on purpose so every metric here is derived in SQL.
CREATE TABLE customers AS
SELECT
    customer_id,
    customer_segment,
    age,
    gender,
    country,
    city,
    income_bracket,
    loyalty_tier,
    shopping_channel,
    device_used,
    payment_method,
    tenure_months,
    total_purchases,
    avg_order_value_usd,
    total_spent_usd,
    days_since_last_purchase,
    return_count,
    complaint_count,
    satisfaction_score,
    customer_acquisition_cost_usd AS cac_usd,
    days_since_last_purchase > 60 AS is_churned   -- same 60-day rule as project 4
FROM stg_customers;

CREATE UNIQUE INDEX idx_customers_id ON customers (customer_id);

-- preferred_category_1..3 are a repeating group; unpivot to one row per
-- (customer, category, rank) so categories can be joined and aggregated.
CREATE TABLE customer_categories AS
SELECT customer_id, 1 AS preference_rank, preferred_category_1 AS category
FROM stg_customers WHERE preferred_category_1 IS NOT NULL
UNION ALL
SELECT customer_id, 2, preferred_category_2
FROM stg_customers WHERE preferred_category_2 IS NOT NULL
UNION ALL
SELECT customer_id, 3, preferred_category_3
FROM stg_customers WHERE preferred_category_3 IS NOT NULL;

CREATE INDEX idx_categories_customer ON customer_categories (customer_id);
