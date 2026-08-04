from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, trim
from pyspark.sql.types import StringType

erp_px_cat_g1v2_rename_map = {
    "ID": "category_id",
    "CAT": "category",
    "SUBCAT": "subcategory",
    "MAINTENANCE": "maintenance"
}

erp_px_cat_g1v2_type_map = {
    "category_id": "string",
    "category": "string",
    "subcategory": "string",
    "maintenance": "string"
}


def transform_erp_px_cat_g1v2(df_bronze: DataFrame) -> DataFrame:
    df_silver = df_bronze.withColumnsRenamed(erp_px_cat_g1v2_rename_map)

    df_silver = df_silver.withColumns({
        field.name: trim(col(field.name)) 
        if isinstance(field.dataType, StringType)
        else col(field.name) 
        for field in df_silver.schema
    })

    df_silver = df_silver.withColumn("_cleaned_at", current_timestamp())

    return df_silver
