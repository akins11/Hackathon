from pandas import DataFrame, Series, to_datetime, merge
from numpy import where
from plotnine import (
    ggplot, geom_col, aes, labs, theme, theme_minimal,
    geom_line, coord_flip, scale_x_discrete, scale_color_manual,
    scale_fill_manual, element_text
)

import warnings
warnings.filterwarnings("ignore")

from typing import Dict, List, Tuple



def filter_department(df:DataFrame, department_name:str) -> Dict[bool, DataFrame]:
    """ """
    try:
        filt_df =  df.loc[df["department"] == department_name]
        return {"error": False, "data": filt_df}
    except ValueError as e:
        print(e)
        return {"error": True, "data": None}


def count_household(filterd_data:DataFrame) -> Dict[bool, int]:
    """ 
    Total household in a department
    """
    try:
        count = filterd_data["household_id"].nunique()
        return {"error": False, "value": count}
    except ValueError as e:
        print(e)
        return {"error": True, "value": None}


def calculate_avg_processed_product(filtered_data:DataFrame) -> Dict[bool, float]:
    """ 
    """
    try:
        avg = filtered_data["number_of_products_processed"].mean().round(1)
        return {"error": False, "value": avg}
    
    except ValueError as e:
        print(e)
        return {"error": True, "value": None}


def percent_perform_irrigation(filtered_data:DataFrame) -> Dict[bool, float]:
    """ 
    Percentage of household that performes irrigation
    """
    try:
        percent = filtered_data["irrigation_practice_on_household_farm"].value_counts(normalize=True).sort_values()[1]
        percent = round(percent*100, 1)
        return {"error": False, "value": percent}
    except ValueError as e:
        print(e)
        return {"error": True, "value": None}


def most_used_source_water(filtered_data:DataFrame) -> Dict[bool, str]:
    """ 
    Most used water source
    """
    try:
        output = (
            filtered_data
                .loc[filtered_data["source_of_irrigation_water_used"] != "NA"]["source_of_irrigation_water_used"]
                .value_counts(sort=True)
                .index[0]
        )
        return {"error": False, "value": output}
    except ValueError as e:
        print(e)
        return {"error": True, "value": None}


def crop_department_count(db_data:DataFrame, prod_cn:DataFrame) -> Dict[bool, ggplot]:
    """ 
    Count of each crop farmed by household
    """
    try:
        func_df = (
            merge(db_data[["department", "household_id"]], prod_cn[["household_id", "crop_name"]], on="household_id", how="left")
            .groupby("department")["crop_name"]
            .value_counts().reset_index()
            .groupby("department")["count"].sum().reset_index()
            .sort_values("count", ascending=True)
        )

        ordered_list = func_df["department"].value_counts().index.tolist()
        fig = (
            ggplot(func_df, aes(x="department", y="count")) +
            geom_col(fill="#64B6AC") +
            coord_flip() +
            scale_x_discrete(limits = ordered_list) +
            labs(x="Department", y="Number of Crops", title="Number of Selected product in each department") +
            theme_minimal() +
            theme(
                figure_size=(8, 5), 
                text=element_text(color="#424242", weight="normal"),
                title=element_text(size=9),
                axis_text=element_text(size=8)
            )
        )
        return {"error": False, "plot": fig}
    except ValueError as e:
        print(e)
        return {"error": True, "plot": ggplot()}


def irrigation_practice_by_household(db_data:DataFrame) -> Dict[bool, ggplot]:
    """ 
    Number of households by department involved in irrigation vs those not involved.
    """
    try:
        func_df = (
            db_data[["department", "household_id", "irrigation_practice_on_household_farm"]]
            .groupby(["department", "irrigation_practice_on_household_farm"])["household_id"]
            .count().reset_index()
            .assign(
                irrigation_practice_on_household_farm = lambda _: where(
                    _["irrigation_practice_on_household_farm"] == 1, "Yes", "No"
                )
            ).sort_values(by=["household_id", "department"]).reset_index()
        )

        ordered_list = func_df["department"].value_counts().index.tolist()
        fig = (
            ggplot(func_df, aes(x="department", y="household_id", fill="irrigation_practice_on_household_farm")) +
            geom_col() +
            coord_flip() +
            scale_x_discrete(limits = ordered_list) +
            scale_fill_manual(values=["#FCAB64", "#64B6AC"])  +
            labs(
                x="Department", 
                y="Number of Households", 
                title="Number of Households that Practice Irrigation", 
                fill="Practice irrigation"
            ) +
            theme_minimal() +
            theme(
                figure_size=(8, 5), 
                text=element_text(color="#424242", weight="normal"),
                plot_title=element_text(ha="left"),
                axis_title=element_text(size=10)
            )
        )

        return {"error": False, "plot": fig}
    except ValueError as e:
        print(e)
        return {"error": True, "plot": ""}


def root_tubers_share(db_data:DataFrame) -> Dict[bool, ggplot]:
    """ 
    Average share of roots & tubers consumed and sold by department.
    """
    try:
        rt_cols = ["share_of_roots_and_tubers_consumed", "share_of_roots_and_tubers_sold"]
        func_df = (
            db_data[["department"]+rt_cols]
            .groupby("department")[rt_cols]
            .agg("mean").reset_index()
            .assign(
                share_of_roots_and_tubers_consumed = lambda _: round(_["share_of_roots_and_tubers_consumed"]*100, 2),
                share_of_roots_and_tubers_sold = lambda _: round(_["share_of_roots_and_tubers_sold"]*100, 2)
            )
            .rename(columns={rt_cols[0]: "Consumed", rt_cols[1]: "Sold"})
            .melt(id_vars=["department"], value_vars=["Consumed", "Sold"], var_name="share_root_tuber")
        )

        ordered_list = func_df["department"].value_counts().index.tolist()
        fig = (
            ggplot(func_df, aes(x="department", y="value", fill="share_root_tuber")) +
            geom_col() +
            coord_flip() +
            scale_x_discrete(limits = ordered_list) +
            labs(
                x="Department", 
                y="Proportion", 
                title="Proportion of Root & Tubers Harvest", 
                fill="Share of Output"
            ) +
            scale_fill_manual(values=["#FCAB64", "#64B6AC"])  +
            theme_minimal() +
            theme(
                figure_size=(8, 5), 
                text=element_text(color="#424242", weight="normal"),
                plot_title=element_text(ha="left"),
                axis_title=element_text(size=10)
            )
        )

        return {"error": False, "plot": fig}
    except ValueError as e:
        print(e)
        return {"error": True, "plot": ggplot()}


def households_use_irrigation_on_crops(filterd_data:DataFrame, prod_cn:DataFrame) -> Dict[bool, DataFrame]:
    """
    Percentage of household across department that used irrigation for different crops. 
    """
    try:
        func_df = (
            merge(
                filterd_data[["department", "household_id", "irrigation_practice_on_household_farm"]],
                prod_cn[["household_id", "crop_name"]],
                on="household_id",
                how="left"
            )
            .groupby(["department", "crop_name"])["irrigation_practice_on_household_farm"]
            .value_counts()
            .reset_index()
            .assign(
                irrigation_practice_on_household_farm = lambda _: where(
                    _["irrigation_practice_on_household_farm"] == 1, "Yes", "No"
                )
            )
            .assign(percentage = lambda _: round(_["count"] / _["count"].sum()*100, 1))
        )[["crop_name", "irrigation_practice_on_household_farm", "count", "percentage"]]

        func_df.columns = ["Crop Name", "Practice Irrigation", "No. Households", "Proportion"]
        return {"error": False, "data": func_df}
    except ValueError as e:
        print(e)
        return {"error": True, "data": None}


# rainfall_df = pd.read_csv("../rainfall_forecasting/data/rainfall_quantity.csv")
def create_forecast_plot(
        all_forecast:DataFrame,
        department:str,
        plot_output:str
) -> Dict[bool, ggplot]:
    """ """

    if plot_output not in ["all", "historical", "forecast"]:
        raise ValueError("`plot_output` must be any of ['all', 'historical', 'forecast']")
    
    history_color = "#0CA4A5"
    forecast_color = "#FDC100"

    try:
        if plot_output == "all":
            fig = (
                ggplot(all_forecast, aes(x="ds", y="y", color="data_type")) +
                geom_line() +
                labs(
                    x="Date", 
                    y="Rainfall Qty.", 
                    title=f"{department} Department Historical & Forecate RainFall Quantity", 
                    color="Period"
                ) +
                scale_color_manual(values=[forecast_color, history_color])  
            )
        elif plot_output == "historical":
            fig = (
                ggplot(all_forecast.query("data_type == 'History'")[["ds", "y"]], aes(x="ds", y="y")) +
                geom_line(color=history_color) +
                labs(
                    x="Date", 
                    y="Rainfall Qty.", 
                    title=f"{department} Department Historical RainFall Quantity", 
                    color="Period"
                ) 
            )
        else:
            fig = (
                ggplot(all_forecast.query("data_type == 'Forecast'")[["ds", "y"]], aes(x="ds", y="y")) +
                geom_line(color=forecast_color) +
                labs(
                    x="Date", 
                    y="Predicted Rainfall Qty.", 
                    title=f"{department} Department RainFall Quantity Forecate",
                    color="Period"
                ) 
            )
        fig = (
            fig + 
            theme_minimal() +
            theme(
                figure_size=(8, 5), 
                text=element_text(color="#424242", weight="normal"),
                plot_title=element_text(ha="left"),
                axis_title=element_text(size=10)
            ) 
        )
        return {"error": False, "plot": fig}
    except ValueError as e:
        print(e)
        return {"error": False, "plot": fig}


def calculate_yoy(forecast_df:DataFrame, data_type:str="History") -> Dict[bool, float]:
    """ """ 
    try:
        highest_month = forecast_df.loc[forecast_df["y"] == forecast_df["y"].max()]["month"].values[0]
        func_df = (
            forecast_df
                .query(f"month == {highest_month} and data_type == '{data_type}'")
                .reset_index(drop=True).sort_values(by="ds", ascending=True).tail(2)
        )[["y", "year"]]

        yoy_qty = (
            func_df.assign(lag_y = lambda _:_["y"].shift(1), 
                            yoy = lambda _: ((_["y"] - _["lag_y"]) / _["lag_y"])*100)["yoy"].values[1]
        )
        return {"error": False, "value": yoy_qty, "yr_highest_month": highest_month}
    
    except ValueError as e:
        print(e)
        return {"error": True, "value": None, "yr_highest_month": None}, 


def calculate_mom(forecast_df:DataFrame, data_type:str="History") -> Dict[bool, float]:
    """ """
    try:
        forecast_df = forecast_df.query(f"data_type == '{data_type}'")

        highest_month = forecast_df.loc[forecast_df["y"] == forecast_df["y"].max()]["month"].values[0]
        latest_year = forecast_df.loc[forecast_df["year"] == forecast_df["year"].max()]["year"].unique()[0]

        fun_df = forecast_df.query(f"year == {latest_year} and month in {[highest_month, highest_month-1]}")[["y", "month"]]
        mom = fun_df.assign(y_lag = lambda _: _["y"].shift(1), 
                      mom = lambda _: ((_["y"] - _["y_lag"]) / _["y_lag"])*100)["mom"].values[1]

        return {"error": False, "value": mom, "month_highest": highest_month}
    except ValueError as e:
        print(e)
        return {"error": True, "value": None, "month_highest": None}