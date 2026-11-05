CREATE OR REPLACE VIEW ecommerce.customer_segments AS

SELECT
    customer_unique_id,

    recency,
    frequency,
    monetary,

    recency_score,
    frequency_score,
    monetary_score,

    CONCAT(
        recency_score,
        frequency_score,
        monetary_score
    ) AS rfm_score,

    CASE
        WHEN recency_score >= 4
             AND frequency_score >= 4
             AND monetary_score >= 4
            THEN 'Champions'

        WHEN recency_score >= 4
             AND frequency_score >= 3
            THEN 'Loyal Customers'

        WHEN recency_score >= 4
             AND frequency_score <= 2
            THEN 'New Customers'

        WHEN recency_score <= 2
             AND frequency_score >= 3
             AND monetary_score >= 3
            THEN 'At Risk'

        WHEN recency_score <= 2
             AND frequency_score <= 2
             AND monetary_score >= 3
            THEN 'High Value At Risk'

        WHEN monetary_score <= 2
            THEN 'Low Value Customers'

        ELSE 'Regular Customers'
    END AS customer_segment

FROM ecommerce.customer_rfm;