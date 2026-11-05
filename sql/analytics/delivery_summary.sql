-- ============================================================
-- DELIVERY SUMMARY
-- ============================================================

CREATE OR REPLACE VIEW ecommerce.delivery_summary AS

SELECT
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'On Time'
    ) AS on_time_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Late'
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Not Delivered'
    ) AS not_delivered_orders,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE delivery_status = 'On Time'
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE delivery_status IN ('On Time', 'Late')
            ),
            0
        ),
        2
    ) AS on_time_percentage,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE delivery_status = 'Late'
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE delivery_status IN ('On Time', 'Late')
            ),
            0
        ),
        2
    ) AS late_percentage,

    ROUND(
        AVG(delivery_days) FILTER (
            WHERE delivery_days IS NOT NULL
        ),
        2
    ) AS average_delivery_days

FROM ecommerce.delivery_performance;