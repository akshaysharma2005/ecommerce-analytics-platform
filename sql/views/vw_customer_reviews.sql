CREATE OR REPLACE VIEW ecommerce.vw_customer_reviews AS

SELECT
    fo.customer_key,
    dc.customer_unique_id,

    COUNT(DISTINCT fr.review_id) AS total_reviews,

    AVG(fr.review_score) AS average_review_score,

    COUNT(
        CASE
            WHEN fr.review_score = 5 THEN 1
        END
    ) AS five_star_reviews,

    COUNT(
        CASE
            WHEN fr.review_score = 4 THEN 1
        END
    ) AS four_star_reviews,

    COUNT(
        CASE
            WHEN fr.review_score = 3 THEN 1
        END
    ) AS three_star_reviews,

    COUNT(
        CASE
            WHEN fr.review_score = 2 THEN 1
        END
    ) AS two_star_reviews,

    COUNT(
        CASE
            WHEN fr.review_score = 1 THEN 1
        END
    ) AS one_star_reviews

FROM ecommerce.fact_reviews fr

JOIN ecommerce.fact_orders fo
    ON fr.order_id = fo.order_id

JOIN ecommerce.dim_customer dc
    ON fo.customer_key = dc.customer_key

GROUP BY
    fo.customer_key,
    dc.customer_unique_id;