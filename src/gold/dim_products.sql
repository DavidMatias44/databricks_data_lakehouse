CREATE OR REPLACE TABLE data_lakehouse.gold.dim_products AS
SELECT
    MD5(cpi.product_key) AS product_sk,
    cpi.product_id,
    cpi.product_key,
    cpi.name,
    epc.category_id,
    epc.category,
    epc.subcategory,
    epc.maintenance,
    cpi.cost,
    cpi.line,
    cpi.start_date,
    CURRENT_TIMESTAMP() AS _created_at
FROM data_lakehouse.silver.crm_prd_info AS cpi
    LEFT JOIN data_lakehouse.silver.erp_px_cat_g1v2 AS epc ON cpi.category_id = epc.category_id
WHERE cpi.end_date = '2099-01-01';
