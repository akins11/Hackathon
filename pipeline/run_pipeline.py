from pandas import DataFrame
from data_import_clean import (
    db_select_columns,
    db_rename_columns,
    db_unique_departments,
    convert_to_int_variables,
    convert_to_float_variables,
    binary_qs_variables_name,

    read_select_variables,
    run_cleaning_transformation_process
)

from save_read_table import save_data_to_database


# Import data from source
try:
    db_data = read_select_variables("data/dummy.csv", db_select_columns, db_rename_columns, db_unique_departments)
except ValueError as e:
    print(e)
    # Create empty dataframe
    db_data = DataFrame()

# Clean & Transform variable
if db_data.shape[0] != 0: 
    try:
        db_cleaned, prod_code_name = run_cleaning_transformation_process(
            db_data,
            db_binary_variables=binary_qs_variables_name,
            db_conv_int_variables=convert_to_int_variables,
            db_conv_float_variables=convert_to_float_variables
        )
    except ValueError as e:
        print(e)
        db_cleaned = DataFrame()
        prod_code_name = DataFrame()

    if db_cleaned.shape[0] != 0 and prod_code_name.shape[0] != 0:
        try:
            save_data_to_database(
                "db\dash_irrigation.duckdb", 
                db_cleaned, 
                "irrigation",
                prod_code_name,
                "prod_code_name"
            )
        except ValueError as e:
            print(e)






