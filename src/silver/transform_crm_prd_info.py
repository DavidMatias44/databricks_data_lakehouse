from pyspark.sql import DataFrame
from pyspark.sql.functions import coalesce, col, current_timestamp, date_sub, lead, length, lit, regexp_replace, substring, trim, upper, when
from pyspark.sql.types import StringType
from pyspark.sql.window import Window


def transform_crm_prd_info(df_bronze: DataFrame, rename_map: dict[str, str], type_map: dict[str, str]) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        for field in df_silver.schema
        if isinstance(field.dataType, StringType)
    })

    df_silver = df_silver.withColumns({
        column: col(column).cast(data_type) 
        for column, data_type in type_map.items()
    })

    df_silver = df_silver.withColumns({
        "product_key": substring(col("product_key"), 7, length(col("product_key"))),
        "category_id": regexp_replace(substring(col("product_key"), 1, 5), "-", "_")
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
