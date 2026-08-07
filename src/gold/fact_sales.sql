CREATE OR REPLACE TABLE data_lakehouse.gold.fact_sales AS
SELECT
    MD5(csd.order_number) AS order_sk,
    dp.product_sk,
    dc.customer_sk,
    csd.order_number,
    csd.order_date,
    csd.ship_date,
    csd.due_date,
    csd.sales,
    csd.quantity,
    csd.price,
    CURRENT_TIMESTAMP() AS _created_at
FROM data_lakehouse.silver.crm_sales_details AS csd
    LEFT JOIN data_lakehouse.gold.dim_products dp ON csd.product_key = dp.product_key
    LEFT JOIN data_lakehouse.gold.dim_customers dc ON csd.customer_id = dc.customer_id;
