import logging

from pyspark.sql.functions import current_timestamp, input_file_name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("bronze_script")

file_paths = [
    "crm/cust_info.csv",
    "crm/prd_info.csv",
    "crm/sales_details.csv",
    "erp/CUST_AZ12.csv",
    "erp/LOC_A101.csv",
    "erp/PX_CAT_G1V2.csv"
]

source_prefix = "/Volumes/data_lakehouse/raw/source_systems/"
target_prefix = "data_lakehouse.bronze."

for file_path in file_paths:
    logger.info(f"Processing file: {source_prefix}{file_path}")
    table_name = file_path.replace("/", "_").replace(".csv", "").lower()

    try:
        df = (
            spark.read
            .option("header", "true")
            .csv(f"{source_prefix}{file_path}")
        )

        df_bronze = df.withColumn("_ingested_at", current_timestamp())
        df_bronze.write.mode("overwrite").saveAsTable(f"{target_prefix}{table_name}")

        logger.info(f"File processed successfully. Written into: {target_prefix}{table_name}")
    except Exception as e:
        logger.exception(f"An error occurred while processing file: {source_prefix}{file_path}")
