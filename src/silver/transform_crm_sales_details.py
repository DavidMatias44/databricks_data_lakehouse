from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, round, trim, try_to_date, when
from pyspark.sql.types import StringType


def transform_crm_sales_details(df_bronze: DataFrame, rename_map: dict[str, str], type_map: dict[str, str]) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        if isinstance(field.dataType, StringType)
        else col(field.name) 
        for field in df_silver.schema
    })

    df_silver = df_silver.withColumns({
        column: col(column).cast(data_type) for column, data_type in type_map.items()
    })

    date_columns = ["order_date", "ship_date", "due_date"]
    df_silver = df_silver.withColumns({
        column: try_to_date(col(column), "yyyyMMdd")
        for column in date_columns
    })

    df_silver = df_silver\
        .withColumn(
            "price",
             when(
                (col("price").isNull()) | (col("price") <= 0),
                round(col("sales") / col("quantity"), 2).cast("decimal(10,2)")
            )
            .otherwise(col("price"))
        )\
        .withColumn(
            "sales",
             when(
                (col("sales").isNull()) | (col("sales") <= 0),
                (col("quantity") * col("price")).cast("decimal(10,2)")
            )
            .otherwise(col("sales"))
        )\
        .withColumn("_cleaned_at", current_timestamp())

    return df_silver
