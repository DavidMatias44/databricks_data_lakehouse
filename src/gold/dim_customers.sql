CREATE OR REPLACE TABLE data_lakehouse.gold.dim_customers AS
SELECT
    MD5(CAST(cci.customer_id AS STRING)) AS customer_sk,
    cci.customer_id,
    cci.customer_key,
    cci.first_name,
    cci.last_name,
    ela.country,
    cci.marital_status,
    CASE
        WHEN cci.gender != 'N/A' THEN cci.gender
        ELSE COALESCE(eca.gender, 'N/A')
    END AS gender,
    eca.birth_date,
    cci.create_date,
    CURRENT_TIMESTAMP() AS _created_at
FROM data_lakehouse.silver.crm_cust_info AS cci
    LEFT JOIN data_lakehouse.silver.erp_cust_az12 AS eca ON cci.customer_key = eca.customer_key
    LEFT JOIN data_lakehouse.silver.erp_loc_a101  AS ela ON cci.customer_key = ela.customer_key
