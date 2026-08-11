crm_cust_info = {
    "cst_id": "customer_id",
    "cst_key": "customer_key",
    "cst_firstname": "first_name",
    "cst_lastname": "last_name",
    "cst_marital_status": "marital_status",
    "cst_gndr": "gender",
    "cst_create_date": "create_date"
}

crm_prd_info = {
    "prd_id": "product_id",
    "prd_key": "product_key",
    "prd_nm": "name",
    "prd_cost": "cost",
    "prd_line": "line",
    "prd_start_dt": "start_date",
    "prd_end_dt": "end_date"
}

crm_sales_details = {
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

erp_cust_az12 = {
    "CID": "customer_key",
    "BDATE": "birth_date",
    "GEN": "gender"
}

erp_loc_a101 = {
    "CID": "customer_key",
    "CNTRY": "country"
}

erp_px_cat_g1v2 = {
    "ID": "category_id",
    "CAT": "category",
    "SUBCAT": "subcategory",
    "MAINTENANCE": "maintenance"
}

rename_maps = {
    "crm_cust_info": crm_cust_info,
    "crm_prd_info": crm_prd_info,
    "crm_sales_details": crm_sales_details,
    "erp_cust_az12": erp_cust_az12,
    "erp_loc_a101": erp_loc_a101,
    "erp_px_cat_g1v2": erp_px_cat_g1v2
}


def get_rename_map(table_name: str) -> dict[str, str]:
    rename_map = rename_maps.get(table_name)
    if rename_map is None:
        raise KeyError(f"Table {table_name} does not have a rename map")
    
    return rename_map
