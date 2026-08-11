from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, trim, upper, when
from pyspark.sql.types import StringType


def transform_crm_cust_info(df_bronze: DataFrame, rename_map: dict[str, str], type_map: dict[str, str]) -> DataFrame:
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

    df_silver = df_silver\
        .withColumn(
            "marital_status",
             when(upper(col("marital_status")) == "M", "Married")
            .when(upper(col("marital_status")) == "S", "Single")
            .otherwise("N/A")
        )\
        .withColumn(
            "gender",
             when(upper(col("gender")) == "M", "Male")
            .when(upper(col("gender")) == "F", "Female")
            .otherwise("N/A")
        )\
        .withColumn(
            "_cleaned_at", current_timestamp()
        )

    return df_silver
