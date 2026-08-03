from pyspark.sql import DataFrame
from pyspark.sql.functions import coalesce, col, current_date, current_timestamp, length, lit, round, substring, trim, try_to_date, upper, when
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

crm_sales_details_rename_map = {
    "sls_ord_num": "order_number",
    "sls_prd_key": "product_key",
    "sls_cust_id": "customer_id",
    "sls_order_dt": "order_date",
    "sls_ship_dt": "ship_date",
    "sls_due_dt": "due_date",
    "sls_sales": "sales",
    "sls_quantity": "quantity",
    "sls_price": "price"
}

# date columns have special date format
crm_sales_details_type_map = {
    "order_number": "string",
    "product_key": "string",
    "customer_id": "integer",
    "sales": "decimal(10,2)",
    "quantity": "integer",
    "price": "decimal(10,2)"
}

def transform_crm_sales_details(df_bronze: DataFrame) -> DataFrame:
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
