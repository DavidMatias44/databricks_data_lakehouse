# Data Catalog

A description about the gold layer: dimension and fact tables.

## gold_dim_customers

Stores demographic and geographic data about customers.

|Column name    |Data type  |Description                                                    |
|:--------------|:----------|:--------------------------------------------------------------|
|customer_sk    |string     |Surrogate key to identify uniquely each customer               |
|customer_id    |int        |Identifier for each customer                                   |
|customer_key   |string     |Alphanumeric identificer for each customer                     |
|first_name     |string     |The first name of the customer                                 |
|last_name      |string     |The last name of the customer                                  |
|country        |string     |The country of the customer ('Australia')                      |
|gender         |string     |The gender of the customer ('Female', 'Male', 'N/A')           |
|marital_status |string     |The marital status of the customer ('Single', 'Married')       |
|birth_date     |date       |The date of birth of the customer, format: YYYY-MM-DD          |
|create_date    |date       |The date when the customer record was created                  |
|_created_at    |timestamp  |Metadata column                                                |

## gold_dim_products

|Column name    |Data type  |Description                                                    |
|:--------------|:----------|:--------------------------------------------------------------|
|product_sk     |string     |Surrogate key to identify uniquely each product                |
|product_id     |int        |Identifier for each product                                    |
|product_key    |string     |Alphanumeric identifier for each product                       |
|name           |string     |The name of the product                                        |
|category_id    |string     |Identifier for the category of the product                     |
|category       |string     |The name of the category of the product ('Bikes', 'Components')|
|subcategory    |string     |The name of the subcategory of the product ('Mountain Bikes')  |
|maintenance    |string     |Does the product require maintenance? ('Yes', 'No')            |
|cost           |decimal    |The cost of the product                                        |
|line           |string     |The product line/series to which the product belongs ('Road')  |
|start_date     |date       |The date on which the current cost took effect                 |
|_created_at    |timestamp  |Metadata column                                                |

## gold_fact_sales

|Column name    |Data type  |Description                                                    |
|:--------------|:----------|:--------------------------------------------------------------|
|order_number   |string     |Alphanumeric identifier for each sale                          |
|product_sk     |string     |Surrogate key linking the order to the product dimension table |
|customer_sk    |string     |Surrogate key linking the order to the customer dimension table|
|order_date     |date       |The date when the order was placed                             |
|ship_date      |date       |The date when the order was shipped to the customer            |
|due_date       |date       |The date when the order payment was due                        |
|sales          |decimal    |The total monetary value for the order                         |
|quantity       |INT        |The number of units of the product in the order                |
|price          |decimal    |The price per unit of the product in the order                 |
|_created_at    |timestamp  |Metadata column                                                |
