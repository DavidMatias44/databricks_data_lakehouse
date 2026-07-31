from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, trim, upper, when
from pyspark.sql.types import StringType

crm_cust_info_rename_map = {
    "cst_id": "customer_id",
    "cst_key": "customer_key",
    "cst_firstname": "first_name",
    "cst_lastname": "last_name",
    "cst_marital_status": "marital_status",
    "cst_gndr": "gender",
    "cst_create_date": "create_date"
}

crm_cust_info_type_map = {
    "customer_id": "integer",
    "customer_key": "string",
    "first_name": "string",
    "last_name": "string",
    "marital_status": "string",
    "gender": "string",
    "create_date": "date",
}

def transform_crm_cust_info(df_bronze: DataFrame) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(crm_cust_info_rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        for field in df_silver.schema
        if isinstance(field.dataType, StringType)
    })

    df_silver = df_silver.withColumns({
        column: col(column).cast(data_type)
        for column, data_type in crm_cust_info_type_map.items()
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
