from pandas import DataFrame, read_csv, Series, concat
from numpy import where
# from polars import read_csv, col
from string import punctuation
from typing import List, Tuple, Dict


# variables 
db_select_columns = [
    'MEN_DEPARTURE', 'HOUSEHOLD_ID', 'MEN_404', 'MEN_511', 'MEN_521', 'MEN_522', 'MEN_52311', 'MEN_52321', 
    'MEN_52312', 'MEN_52322', 'MEN_52313', 'MEN_52323', 'MEN_52314', 'MEN_52324', 'MEN_111', 'MEN_1141', 'MEN_1221', 
    'CMEN_12231', 'CMEN_12232', 'MEN_1251', 'MEN_1611', 'MEN_1612', 'MEN_1621', 'MEN_1622'
]

db_rename_columns = [
    'Department', 'Household ID', 'Gender of head of household', 'Crop production', 'Processing of agricultural products',
    'Number of products processed', 'Processed product name 1', 'Processed product code 1', 'Processed product name 2', 
    'Processed product code 2', 'Processed product name 3','Transformed product code 3','Processed product name 4', 
    'Processed product code 4', 'Irrigation practice on household farm', 'Source of irrigation water used', 
    'Number of roots and tubers used', 'Share of roots and tubers consumed', 'Share of roots and tubers sold', 
    'Number of industrial crops grown', 'Use of mineral fertilizers by men', 'Use of mineral fertilizers by women', 
    'Use of organic fertilizers by men', 'Use of organic fertilizers by women'
]

db_unique_departments = [
    'DEPARTURE. BORGOU', 'DEPARTURE. ALIBORI', 'DEPARTURE. ATACORA', 'DEPARTURE. DONGA', 'DEPARTURE. ZOU', 'DEPARTURE. HILLS', 
    'DEPARTURE. MONO', 'DEPARTURE. COUFFO', 'DEPARTURE. OUEME', 'DEPARTURE. PLATEAU', 'DEPARTURE. ATLANTIC', 'DEPARTURE. LITTORAL'
]

convert_to_int_variables = [
    "number_of_products_processed", "processed_product_code_1", "processed_product_code_2", "transformed_product_code_3",
    "processed_product_code_4", "number_of_roots_and_tubers_used", "number_of_industrial_crops_grown"
]
convert_to_float_variables = ["share_of_roots_and_tubers_consumed", "share_of_roots_and_tubers_sold"]

binary_qs_variables_name = [
    "crop_production", "processing_of_agricultural_products", "irrigation_practice_on_household_farm", 
    "use_of_mineral_fertilizers_by_men", "use_of_mineral_fertilizers_by_women", "use_of_organic_fertilizers_by_men", 
    "use_of_organic_fertilizers_by_women"
]


def read_select_variables(
        file_path:str, 
        db_select_variables:List[str], 
        db_rename_variables:List[str],
        db_unq_departments:List[str]
) -> DataFrame:
    """ """

    try:
        db_data = read_csv(file_path, usecols=db_select_variables)[db_select_variables]
        db_data.columns = [str(col).strip().lower().replace(" ", "_") for col in db_rename_variables]
        db_data = db_data.query(f"department in {db_unq_departments}") # -========================== /!\

        # Check number of rows
        if db_data.shape[0] < 1:
            raise ValueError("Data Can not have zero rows")
        # Check number of columns
        if db_data.shape[1] < 24:
            raise ValueError("Data Can not have less than 24 columns")
        
    except ValueError as e:
        print(e)
        db_data = read_csv(file_path)

    return db_data



def handle_binary_variable(df:DataFrame, db_variable:str) -> Series:
    """ """
    func_df = df.copy()

    try:
        if func_df[db_variable].dtype == "bool":
            func_df[db_variable] = func_df[db_variable].astype("int64")

        elif func_df[db_variable].dtype == "int64":
            if func_df[db_variable].nunique() == 2 and all(func_df[db_variable].unique() == [1, 2]):
                func_df[db_variable] = where(func_df[db_variable] == 2, 0, 1)
            else:
                if func_df[db_variable].nunique() > 2:
                    raise ValueError(f"There are more than 2 unique values in {db_variable}. expectes 2")
                
                if not all(func_df[db_variable].unique() == [1, 2]):
                    raise ValueError(f"Unknow binary coding for {db_variable} expected [1, 2] or [0, 1]")
        
        return func_df[db_variable]
    except ValueError as e:
        print(e)
        return func_df[db_variable]


def convert_string_to_numeric(df:DataFrame, db_variable:str, convert_int:bool=True) -> Series:
    """ """
    func_df = df.copy()

    try:
        if func_df[db_variable].dtype == "O":
            for punt in punctuation:
                if punt == '.':
                    func_df[db_variable] = func_df[db_variable].str.replace(r"\.+", ".")
                else:
                    func_df[db_variable] = func_df[db_variable].str.replace(punt, "")

            if convert_int:
                func_df[db_variable] = func_df[db_variable].astype("int64")
            else:
                func_df[db_variable] = func_df[db_variable].astype("float64")
        
        return func_df[db_variable]
    except ValueError as e:
        print(e)
        return func_df[db_variable]
    

def clean_variables(
        df:DataFrame, 
        db_binary_variables:List[str],
        db_conv_int_variables:List[str],
        db_conv_float_variables:List[str]
) -> DataFrame:
    """ """

    try:
        # Clean department variable
        if df["department"].dtypes == "O":
            df["department"] = df["department"].str.replace("DEPARTURE. ", " ").str.strip()
        # Check cleaned output
        # ...

        # Clean gender column
        if df['gender_of_head_of_household'].dtypes == "O" and df['gender_of_head_of_household'].nunique() == 2:
            df['gender_of_head_of_household'] = where(
                df['gender_of_head_of_household'].isin(["M", "m", "male"]), "Male", "Female"
            )
        elif df['gender_of_head_of_household'].dtypes == "int64":
            male_value = df["gender_of_head_of_household"].value_counts(sort=True).index[0]
            df['gender_of_head_of_household'] = where(df['gender_of_head_of_household'] == male_value, "Male", "Female")
        # Check cleaned output
        if not all(value in list(df["gender_of_head_of_household"].unique()) for value in ["Male", "Female"]):
            raise ValueError("`gender_of_head_of_household` variable cleaning failed...")
        
        # Handle water source values
        df["source_of_irrigation_water_used"] = df["source_of_irrigation_water_used"].fillna("NA")
        # Check cleaned output
        if df["source_of_irrigation_water_used"].fillna("NA").isnull().sum() > 1:
            raise ValueError(f"failed to fill `source_of_irrigation_water_used` variable missing values")
        
        # Handle Binary Columns
        for binary_cols in db_binary_variables:
            df[binary_cols] = handle_binary_variable(df, binary_cols)
            # Check cleaned output
            if not all(df[binary_cols].unique() == [1, 0]):
                raise ValueError(f"{binary_cols} variable failed to convert to binary [1, 0]")

        # string to numeric:
        # To Integer
        for int_cols in db_conv_int_variables:
            df[int_cols] = convert_string_to_numeric(df=df, db_variable=int_cols, convert_int=True)
        # Check cleaned output
            if not df[int_cols].dtype == "int64":
                raise ValueError(f"{int_cols} variable failed to convert to Integer")

        # To Float
        for float_cols in db_conv_float_variables:
            df[float_cols] = convert_string_to_numeric(df=df, db_variable=float_cols, convert_int=False)
        # Check cleaned output
            if not df[float_cols].dtype == "float64":
                raise ValueError(f"{float_cols} variable failed to convert to Float")
            
        return df
    except:
        return df
    


def tranform_processed_products_long(df:DataFrame) -> DataFrame:
    """ """
    try:
        code_variables = [col for col in df.columns if "processed_product_code" in col or "transformed_product_code" in col]
        name_variables = [col for col in df.columns if "processed_product_name" in col]

        df_name = df[['household_id']+name_variables].melt(
            id_vars=["household_id"], value_vars=name_variables, var_name="var_name", value_name="crop_name"
        ).rename(columns={"household_id": "household_id_name"})

        df_code = df[['household_id']+code_variables].melt(
            id_vars=["household_id"], value_vars=code_variables, var_name="var_code", value_name="crop_code"
        ).rename(columns={"household_id": "household_id_code"})

        fun_df = concat([df_name, df_code], axis=1)

        # Checks 
        check = (
            fun_df
            .assign(check = lambda _: _["var_code"].str.split("_", expand=True)[3] == _["var_name"].str.split("_", expand=True)[3]) 
            .query("household_id_code == household_id_name and check")
        ).shape[0] == df.shape[0] * 4

        if check:
            fun_df = (
                fun_df
                .drop(["household_id_code", "var_code"], axis=1)
                .rename(columns={'household_id_name': 'household_id', 'var_name': 'product'})
                .assign(crop_code = lambda _: "0" + _['crop_code'].astype("str"))
            )
            # Select only choosen crops. 
            fun_df = fun_df.loc[fun_df["crop_name"].str.lower().isin(["cotton", "yam", "cocoa", "cassava"])]
            return fun_df
        
        else:
            return DataFrame()
    except ValueError as e:
        print(e)
        return DataFrame()
    


def run_cleaning_transformation_process(imp_data:DataFrame, **kwargs) -> Tuple[DataFrame, DataFrame]:
    """ """

    # Clean and check  data
    df = clean_variables(imp_data, **kwargs)

    # Extract product code and name
    product_code_name = tranform_processed_products_long(df)

    # Drop product name and code from cleaned data
    df = df.drop([col for col in df.columns if "processed_product" in col or "transformed_product_code" in col], axis=1)

    return df, product_code_name