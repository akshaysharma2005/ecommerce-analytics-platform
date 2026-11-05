CREATE OR REPLACE VIEW ecommerce.vw_payment_analysis AS

SELECT
    payment_type,

    COUNT(*) AS total_payment_records,

    COUNT(DISTINCT order_id) AS total_orders,

    SUM(payment_value) AS total_payment_value,

    AVG(payment_value) AS average_payment_value,

    AVG(payment_installments) AS average_installments,

    MAX(payment_value) AS maximum_payment_value

FROM ecommerce.fact_payments

GROUP BY
    payment_type;