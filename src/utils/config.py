from pathlib import Path

from silver.transform_crm_cust_info import transform_crm_cust_info
from silver.transform_crm_prd_info  import transform_crm_prd_info
from silver.transform_crm_sales_details import transform_crm_sales_details
from silver.transform_erp_cust_az12 import transform_erp_cust_az12
from silver.transform_erp_loc_a101 import transform_erp_loc_a101
from silver.transform_erp_px_cat_g1v2 import transform_erp_px_cat_g1v2

project_path = Path.cwd().parent
raw_data_path = project_path / "data"
raw_volume_path = Path("/Volumes/data_lakehouse/raw/source_systems")

raw_file_paths = [
    item for item in raw_volume_path.glob("*/*.csv")
    if item.is_file()
]

silver_config = {
    "crm_cust_info": transform_crm_cust_info,
    "crm_prd_info": transform_crm_prd_info,
    "crm_sales_details": transform_crm_sales_details,
    "erp_cust_az12": transform_erp_cust_az12,
    "erp_loc_a101": transform_erp_loc_a101,
    "erp_px_cat_g1v2": transform_erp_px_cat_g1v2
}

bronze_schema_path = "data_lakehouse.bronze."
silver_schema_path = "data_lakehouse.silver."
