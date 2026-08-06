import logging

from utils.config import bronze_schema_path, silver_config, silver_schema_path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("silver_script")


def run_silver_pipeline():
    for table_name, transform_function in silver_config.items():
        try:
            logger.info(f"Reading Bronze table: {bronze_schema_path}{table_name}")
            df_bronze = spark.table(f"{bronze_schema_path}{table_name}")

            logger.info(f"Processing Bronze table: {bronze_schema_path}{table_name}")
            df_silver = df_bronze.transform(transform_function)

            df_silver.write.mode("overwrite").saveAsTable(f"{silver_schema_path}{table_name}")
            logger.info(f"Bronze table processed successfully. Written into: {silver_schema_path}{table_name}")
        except Exception as e:
            logger.exception(f"Could not process Bronze table: {bronze_schema_path}{table_name}")


if __name__ == "__main__":
    run_silver_pipeline()
