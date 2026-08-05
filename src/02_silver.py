import logging

from silver.transform_crm_cust_info import transform_crm_cust_info
from silver.transform_crm_prd_info  import transform_crm_prd_info
from silver.transform_crm_sales_details import transform_crm_sales_details
from silver.transform_erp_cust_az12 import transform_erp_cust_az12
from silver.transform_erp_loc_a101 import transform_erp_loc_a101
from silver.transform_erp_px_cat_g1v2 import transform_erp_px_cat_g1v2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("silver_script")

bronze_prefix = "data_lakehouse.bronze."
silver_prefix = "data_lakehouse.silver."

silver_config = {
    f"{bronze_prefix}crm_cust_info": (transform_crm_cust_info, f"{silver_prefix}crm_cust_info"),
    f"{bronze_prefix}crm_prd_info":  (transform_crm_prd_info, f"{silver_prefix}crm_prd_info"),
    f"{bronze_prefix}crm_sales_details":  (transform_crm_sales_details, f"{silver_prefix}crm_sales_details"),
    f"{bronze_prefix}erp_cust_az12":  (transform_erp_cust_az12, f"{silver_prefix}erp_cust_az12"),
    f"{bronze_prefix}erp_loc_a101":  (transform_erp_loc_a101, f"{silver_prefix}erp_loc_a101"),
    f"{bronze_prefix}erp_px_cat_g1v2":  (transform_erp_px_cat_g1v2, f"{silver_prefix}erp_px_cat_g1v2")
}


def run_silver_pipeline():
    for bronze_table, (transform_function, silver_table) in silver_config.items():
        try:
            logger.info(f"Reading Bronze table: {bronze_table}")
            df_bronze = spark.table(bronze_table)

            logger.info(f"Processing Bronze table: {bronze_table}")
            df_silver = df_bronze.transform(transform_function)

            df_silver.write.mode("overwrite").saveAsTable(silver_table)
            logger.info(f"Bronze table processed successfully. Written into: {silver_table}")
        except Exception as e:
            logger.exception(f"Could not process Bronze table: {bronze_prefix}{bronze_table}")


if __name__ == "__main__":
    run_silver_pipeline()
