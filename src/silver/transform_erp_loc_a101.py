from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, regexp_replace, trim, upper, when
from pyspark.sql.types import StringType

erp_loc_a101_rename_map = {
    "CID": "customer_key",
    "CNTRY": "country"
}

erp_loc_a101_type_map = {
    "customer_key": "string",
    "country": "string"
}


def transform_erp_loc_a101(df_bronze: DataFrame) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(erp_loc_a101_rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        if isinstance(field.dataType, StringType)
        else col(field.name)
        for field in df_silver.schema
    })

    df_silver = df_silver\
        .withColumn(
            "customer_key",
            regexp_replace(col("customer_key"), "-", "")
        )\
        .withColumn(
            "country",
             when(upper(col("country")) == "DE", "Germany")
            .when((upper(col("country")) == "USA") | (upper(col("country")) == "US"), "United States")
            .when((col("country").isNull()) | (col("country") == ""), "N/A")
            .otherwise(col("country"))
        )\
        .withColumn("_cleaned_at", current_timestamp())

    return df_silver
