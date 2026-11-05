CREATE OR REPLACE VIEW ecommerce.customer_segment_summary AS

SELECT
    customer_segment,

    COUNT(*) AS total_customers,

    ROUND(
        AVG(recency),
        2
    ) AS average_recency,

    ROUND(
        AVG(frequency),
        2
    ) AS average_frequency,

    ROUND(
        AVG(monetary),
        2
    ) AS average_monetary,

    ROUND(
        SUM(monetary),
        2
    ) AS total_customer_spending

FROM ecommerce.customer_segments

GROUP BY
    customer_segment

ORDER BY
    total_customer_spending DESC;