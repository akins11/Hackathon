from pandas import DataFrame

def get_unique_values_list(data:DataFrame, value_type:str, by_var:str=None, by_value:str=None):
    """ """
    try:
        if by_var is None:
            val = list(data[value_type].unique())
        else:
            if by_value is not None:
                val = list(data.query(f"{by_var} == '{by_value}'")[value_type].unique())
        return {"error": False, "value": val}
    except ValueError as e:
        print(e)
        return {"error": True, "value": None}