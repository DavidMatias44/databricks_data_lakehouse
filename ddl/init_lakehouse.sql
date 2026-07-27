CREATE CATALOG IF NOT EXISTS data_lakehouse
COMMENT 'Catalog for the databricks_data_lakehouse project';

USE CATALOG data_lakehouse;

CREATE SCHEMA IF NOT EXISTS bronze
COMMENT 'Schema for the Bronze layer (raw data)';

CREATE SCHEMA IF NOT EXISTS silver
COMMENT 'Schema for the Silver layer (cleaned and standardized data)';

CREATE SCHEMA IF NOT EXISTS gold
COMMENT 'Schema for the Gold layer (business ready data)';

CREATE SCHEMA IF NOT EXISTS raw
COMMENT 'Schema for the source CSV files (CRM and ERP)';

CREATE VOLUME IF NOT EXISTS raw.source_systems
COMMENT 'Volume for the source CSV files (CRM and ERP)';
