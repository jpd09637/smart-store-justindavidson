import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    
    cursor.execute("DROP TABLE IF EXISTS customer")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    region TEXT,
    join_date TEXT,
    loyalty_pts INTEGER,
    preferred_contact_method TEXT
    )
    """)

    cursor.execute("DROP TABLE IF EXISTS product")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unitprice FLOAT,
            stock_quantity INTEGER,
            preferred_customer_discount_applicable TEXT
        )
    """)

    cursor.execute("DROP TABLE IF EXISTS sale")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    sale_amount FLOAT,
    sale_date TEXT,
    amt_sold_fiscal_year INTEGER,
    payment_type TEXT,
    store_id INTEGER,
    campaign_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)
def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_prepared.csv"))

        customers_df.columns = [col.lower() for col in customers_df.columns]
        customers_df = customers_df.rename(columns={
    "customerid": "customer_id",
    "name": "name",
    "region": "region",
    "joindate": "join_date",
    "loyaltypts": "loyalty_pts",
    "preferredcontactmethod": "preferred_contact_method"
})
        products_df.columns = [col.lower() for col in products_df.columns]
        products_df = products_df.rename(columns={
    "productid": "product_id",
    "productname": "product_name", 
    "category": "category",
    "unitprice": "unitprice",
    "stockquantity": "stock_quantity",
    "preferredcustomerdiscountapplicable": "preferred_customer_discount_applicable"
})
        sales_df.columns = [col.lower() for col in sales_df.columns]
        sales_df = sales_df.rename(columns={
    "transactionid": "transaction_id",
    "customerid": "customer_id",
    "productid": "product_id",
    "saleamount": "sale_amount",
    "saledate": "sale_date",
    "amtsoldfiscalyear": "amt_sold_fiscal_year",
    "payment_type": "payment_type",
    "storeid": "store_id",
    "campaignid": "campaign_id"
})

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()