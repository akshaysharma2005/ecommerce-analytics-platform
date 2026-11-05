CREATE OR REPLACE VIEW ecommerce.review_summary AS
SELECT
    review_score,
    COUNT(*) AS total_reviews,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM ecommerce.fact_reviews
GROUP BY review_score
ORDER BY review_score DESC;