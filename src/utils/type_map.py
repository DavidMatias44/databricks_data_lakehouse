crm_cust_info = {
    "customer_id": "integer",
    "customer_key": "string",
    "first_name": "string",
    "last_name": "string",
    "marital_status": "string",
    "gender": "string",
    "create_date": "date",
}

crm_prd_info = {
    "product_id": "integer",
    "product_key": "string",
    "name": "string",
    "cost": "decimal(10,2)",
    "line": "string",
    "start_date": "date",
    "end_date": "date"
}

# date columns have special date format
crm_sales_details = {
    "order_number": "string",
    "product_key": "string",
    "customer_id": "integer",
    "sales": "decimal(10,2)",
    "quantity": "integer",
    "price": "decimal(10,2)"
}

erp_cust_az12 = {
    "customer_key": "string",
    "birth_date": "date",
    "gender": "string"
}

erp_loc_a101 = {
    "customer_key": "string",
    "country": "string"
}

erp_px_cat_g1v2 = {
    "category_id": "string",
    "category": "string",
    "subcategory": "string",
    "maintenance": "string"
}

type_maps = {
    "crm_cust_info": crm_cust_info,
    "crm_prd_info": crm_prd_info,
    "crm_sales_details": crm_sales_details,
    "erp_cust_az12": erp_cust_az12,
    "erp_loc_a101": erp_loc_a101,
    "erp_px_cat_g1v2": erp_px_cat_g1v2
}


def get_type_map(table_name: str) -> dict[str, str]:
    type_map = type_maps.get(table_name)
    if type_map is None:
        raise KeyError(f"Table {table_name} does not have a type map")

    return type_map
