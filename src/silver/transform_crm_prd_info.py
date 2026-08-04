from pyspark.sql import DataFrame
from pyspark.sql.functions import coalesce, col, current_timestamp, date_sub, lead, length, lit, substring, trim, upper, when
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

crm_prd_info_rename_map = {
    "prd_id": "product_id",
    "prd_key": "product_key",
    "prd_nm": "name",
    "prd_cost": "cost",
    "prd_line": "line",
    "prd_start_dt": "start_date",
    "prd_end_dt": "end_date"
}

crm_prd_info_type_map = {
    "product_id": "integer",
    "product_key": "string",
    "name": "string",
    "cost": "decimal(10,2)",
    "line": "string",
    "start_date": "date",
    "end_date": "date"
}


def transform_crm_prd_info(df_bronze: DataFrame) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(crm_prd_info_rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        for field in df_silver.schema
        if isinstance(field.dataType, StringType)
    })

    df_silver = df_silver.withColumns({
        column: col(column).cast(data_type) 
        for column, data_type in crm_prd_info_type_map.items()
    })

    df_silver = df_silver.withColumns({
        "product_key": substring(col("product_key"), 7, length(col("product_key"))),
        "category_id": substring(col("product_key"), 1, 5)
    })

    window_spec = Window.partitionBy("product_key").orderBy("start_date")

    df_silver = df_silver\
        .withColumn(
            "cost", coalesce(col("cost"), lit(0))
        )\
        .withColumn(
            "line",
             when(upper(col("line")) == "M", "Mountain")
            .when(upper(col("line")) == "R", "Road")
            .when(upper(col("line")) == "S", "Other Sales")
            .when(upper(col("line")) == "T", "Touring")
            .otherwise("N/A")
        )\
        .withColumn(
            "end_date",
            coalesce(date_sub(lead(col("start_date")).over(window_spec), 1), lit("2099-01-01"))
        )\
        .withColumn(
            "is_current",
            col("end_date") == lit("2099-01-01")
        )

    cols = df_silver.columns
    for column in ["end_date", "product_key"]:
        target_index = cols.index(column)
        cols.insert(target_index + 1, cols.pop())
    df_silver = df_silver.select(*cols)
    
    df_silver = df_silver.withColumn("_cleaned_at", current_timestamp())

    return df_silver
