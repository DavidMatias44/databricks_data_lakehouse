import logging

from pyspark.sql.functions import current_timestamp, input_file_name

from utils.config import raw_file_paths, bronze_schema_path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("bronze_script")


def run_bronze_pipeline():
    for raw_file_path in raw_file_paths:
        logger.info(f"Processing file: {raw_file_path}")

        system_name = raw_file_path.parent.name
        raw_file_name = raw_file_path.name.replace(".csv", "").lower()
        table_name = f"{system_name}_{raw_file_name}"

        try:
            df = (
                spark.read
                .option("header", "true")
                .csv(f"{raw_file_path}")
            )

            df_bronze = df.withColumn("_ingested_at", current_timestamp())
            df_bronze.write.mode("overwrite").saveAsTable(f"{bronze_schema_path}{table_name}")
            logger.info(f"File processed successfully. Written into: {bronze_schema_path}{table_name}")
        except Exception as e:
            logger.exception(f"An error occurred while processing file: {raw_file_path}")


if __name__ == "__main__":
    run_bronze_pipeline()
