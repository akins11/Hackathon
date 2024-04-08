from pandas import DataFrame, read_sql
import duckdb

import warnings
warnings.filterwarnings("ignore")

def save_data_to_database(
        new_database_path:str, 
        cleaned_data:DataFrame, 
        cleaned_data_table_name:str,
        prod_name_code:DataFrame,
        prod_name_code_table_name:str,
):
    """ """
    # Create new duckdb database
    conn = duckdb.connect(database=new_database_path) 

    # Move data into database
    cleaned_data.to_sql(cleaned_data_table_name, conn, index=False)
    prod_name_code.to_sql(prod_name_code_table_name, conn, index=False) 

    # Close connection
    conn.close()



def read_data_from_database(database_path:str, table_name:str) -> DataFrame:
    """ """
    # Create a new connection to database
    new_conn = duckdb.connect(database=database_path) 

    db_table = read_sql(f"SELECT * FROM {table_name}", new_conn)

    # Close connection
    new_conn.close()

    return db_table