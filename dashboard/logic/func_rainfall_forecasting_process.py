from pandas import DataFrame, to_datetime, concat
import calendar

import matplotlib.pyplot as plt
from seaborn import lineplot

from prophet import Prophet

from sklearn.metrics import mean_squared_error, mean_absolute_error

import warnings
warnings.filterwarnings("ignore")


def clean_rainfall_data(raw_rainfall_data: DataFrame) -> DataFrame:
    """
    :params
     raw_rainfall_data: Imported rainfall quantity dataset to clean.
    :retun 
     A cleaned pandas dataframe with the following columns.
        "department": object = Names of the cleaned department.
        "date": datetime64[ns]= date period (year-month)
        "rainfall_qty": float64= Total quantity of rainfall within the period.
        "year": int64=The year the data was collected.
        "month_name": object=Names of the month.
        "month": int64= The month id.
    """

    # Check that a pandas dataframe is supplied as the `raw_rainfall_data`. 
    if not isinstance(raw_rainfall_data, DataFrame):
        raise ValueError("data supplied must be a pandas.DataFrame")
    
    try:
        # Copy raw_rainfall_data to func_df
        func_df = raw_rainfall_data.copy()

        # Get a list of all month names.
        month_name = list(calendar.month_name)[1:]
        
        # Clean rainfall quantity data.
        func_df = (
            func_df
                .drop(["Total ", "Average"], axis=1)                                                  
                .melt(                                                                               
                    id_vars=["Communities", "Year"], 
                    value_vars=month_name,
                    var_name="month_name",
                    value_name="rainfall_qty"
                )
                .rename(columns={"Communities": "department", "Year": "year"})                         
                .assign(
                    department = lambda _: _["department"].str.replace(r"(\bDEPARTURE\.|DEAPRTURE\.)", "", regex=True).str.strip(),  
                    month = lambda _: _["month_name"].map({value: indx+1 for indx, value in enumerate(month_name)}), 
                    str_date = lambda _: _["year"].astype("str") + "-" + _["month"].astype("str"),   
                    date = lambda _: to_datetime(_["str_date"], format="%Y-%m")                  
                )
                .query("department != 'BENIGN'")
                .drop("str_date", axis=1)                                                            
        )[["department", "date", "rainfall_qty", "year", "month_name", "month"]]  

        # Check dataframe ....

        return {"error": False, "data": func_df}
    except ValueError as e:
        print(e)
        return {"error": True, "data": None}



def forecast_rainfall_monthly_quantity(
        rainfall_data:DataFrame, 
        department:str, 
        n_future_period:int=24,
        append_new_data:DataFrame=None
):
    """ 
    params:
        rainfall_data: histotical rainfall dataset.
        department: selected department to predict future rainfall quantity.
        n_future_period: Number of future period to predict.
        append_new_data: add new data to the existing dataset.
    return:
        A tupel of length 3 containing  the forecast, historical and Prophet model.
    """

    # Data Preparation
    df = rainfall_data.copy()
    
    try:
        if append_new_data is not None:
            # Check that the first date in the new data is ahead of the last-date in the current data
            if not append_new_data["date"].min() > df["date"].max():
                raise ValueError("New data containes clashing dates with current data.")
            
            try:
                df = concat([df, append_new_data], axis=0)
            except ValueError as e:
                print(f"Unable to append new data.\n{e}")


        fct_df = (
            df
            .query(f"department	== '{department}'")[["date", "rainfall_qty"]]
            .rename(columns={'date':'ds', 'rainfall_qty':'y'})
            .sort_values(by="ds", ascending=True)
            .reset_index(drop=True)
        )
        
        # Fitting
        pp_mdl = Prophet(seasonality_mode="multiplicative")
        # seasonality_mode="multiplicative",
        # yearly_seasonality="auto"

        pp_mdl.fit(fct_df)

        # Forecasting
        future_df = pp_mdl.make_future_dataframe(
            periods=n_future_period, 
            freq='MS', 
            include_history=False
        )

        forecast = pp_mdl.predict(future_df)

        return {"error": False, "values": (forecast, fct_df, pp_mdl)}
    except ValueError as e:
        print(e)
        return {"error": True, "values": (None, None, None)}





def forecast_output(main_df:DataFrame, forecasted_df:DataFrame, output_type:str="table"):
    """ 
    """
    try:
        fct_df = (
            forecasted_df[["ds", "yhat"]].rename(columns={"yhat": "y"}).assign(data_type = "Forecast")
            # Include yhat_lower & yhat_upper 
        )
        main_df = main_df.assign(data_type = "History").copy()

        all_df = concat([main_df, fct_df], axis=0)
        all_df['ds'] = to_datetime(all_df["ds"])
        all_df['year'] = all_df['ds'].dt.year
        all_df['month'] = all_df['ds'].dt.month

        return {"error": False, "data": all_df}
    except ValueError as e:
        print(e)
        return {"error": False, "data": all_df}
