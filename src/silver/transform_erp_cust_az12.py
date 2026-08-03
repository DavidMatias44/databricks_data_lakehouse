from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_date, current_timestamp, length, lit, substring, trim, upper, when
from pyspark.sql.types import StringType

crm_sales_details_rename_map = {
    "CID": "customer_key",
    "BDATE": "birth_date",
    "GEN": "genre"
}

crm_sales_details_type_map = {
    "customer_key": "string",
    "birth_date": "date",
    "genre": "string"
}

def transform_erp_cust_az12(df_bronze: DataFrame) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(crm_sales_details_rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        if isinstance(field.dataType, StringType)
        else col(field.name) 
        for field in df_silver.schema
    })

    df_silver = df_silver.withColumns({
        column: col(column).cast(data_type) for column, data_type in crm_sales_details_type_map.items()
    })

    df_silver = df_silver\
        .withColumn(
            "customer_key",
             when(col("customer_key").like("NAS%"), substring(col("customer_key"), 4, length(col("customer_key"))))
            .otherwise(col("customer_key"))
        )\
        .withColumn(
            "birth_date",
             when((col("birth_date") <= lit("1926-01-01")) | (col("birth_date") >= current_date()), lit(None))
            .otherwise(col("birth_date"))
        )\
        .withColumn(
            "genre",
             when((upper(col("genre")) == "F") | (upper(col("genre")) == "FEMALE"), "Female")
            .when((upper(col("genre")) == "M") | (upper(col("genre")) == "MALE"), "Male")
            .otherwise("N/A")
        )\
        .withColumn("_cleaned_at", current_timestamp())

    return df_silver