-- ============================================================
-- CUSTOMER RETENTION ANALYSIS
-- Member 2: Customer Analytics
-- ============================================================


-- 1. ONE-TIME VS REPEAT CUSTOMERS

SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-time Customers'
        ELSE 'Repeat Customers'
    END AS customer_type,
    COUNT(*) AS total_customers,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM ecommerce.vw_customer_revenue
GROUP BY
    CASE
        WHEN total_orders = 1 THEN 'One-time Customers'
        ELSE 'Repeat Customers'
    END
ORDER BY total_customers DESC;


-- 2. MONTHLY CUSTOMER COHORT RETENTION

WITH customer_months AS (
    SELECT DISTINCT
        customer_unique_id,
        DATE_TRUNC('month', order_date)::date AS purchase_month
    FROM ecommerce.vw_order_revenue
),
first_purchase AS (
    SELECT
        customer_unique_id,
        MIN(purchase_month) AS cohort_month
    FROM customer_months
    GROUP BY customer_unique_id
),
cohort_activity AS (
    SELECT
        fp.cohort_month,
        cm.purchase_month,
        (
            EXTRACT(YEAR FROM AGE(cm.purchase_month, fp.cohort_month)) * 12
            + EXTRACT(MONTH FROM AGE(cm.purchase_month, fp.cohort_month))
        )::integer AS month_number,
        COUNT(DISTINCT cm.customer_unique_id) AS active_customers
    FROM customer_months cm
    JOIN first_purchase fp
        ON cm.customer_unique_id = fp.customer_unique_id
    GROUP BY fp.cohort_month, cm.purchase_month
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(*) AS cohort_size
    FROM first_purchase
    GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    ca.month_number,
    cs.cohort_size,
    ca.active_customers,
    ROUND(
        100.0 * ca.active_customers / cs.cohort_size,
        2
    ) AS retention_percentage
FROM cohort_activity ca
JOIN cohort_sizes cs
    ON ca.cohort_month = cs.cohort_month
ORDER BY ca.cohort_month, ca.month_number;
