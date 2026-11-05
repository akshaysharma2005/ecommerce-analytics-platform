DROP VIEW IF EXISTS ecommerce.customer_rfm;

CREATE VIEW ecommerce.customer_rfm AS

WITH reference_date AS (
    SELECT MAX(last_order_date) AS max_order_date
    FROM ecommerce.vw_customer_revenue
),

rfm_calculation AS (
    SELECT
        cr.customer_unique_id,

        (rd.max_order_date - cr.last_order_date) AS recency,

        cr.total_orders AS frequency,

        cr.total_revenue AS monetary

    FROM ecommerce.vw_customer_revenue cr
    CROSS JOIN reference_date rd
)

SELECT
    customer_unique_id,
    recency,
    frequency,
    monetary,

    NTILE(5) OVER (
        ORDER BY recency DESC
    ) AS recency_score,

    NTILE(5) OVER (
        ORDER BY frequency ASC
    ) AS frequency_score,

    NTILE(5) OVER (
        ORDER BY monetary ASC
    ) AS monetary_score

FROM rfm_calculation;