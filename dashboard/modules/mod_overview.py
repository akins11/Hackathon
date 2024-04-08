from shiny import Inputs, Outputs, Session, module, render, ui, reactive, req

from components.comp_global import filter_dropdowns, ui_column, ui_row
from components.comp_overview import (
    household_count_card, 
    mom_yoy_card,
    metric_output
)
from faicons import icon_svg

from logic.func_data_input import get_unique_values_list
from logic.func_overview_backend import *
from logic.func_rainfall_forecasting_process import forecast_rainfall_monthly_quantity, forecast_output




@module.ui
def overview_ui():
    return ui.TagList(
        # -------------------------------------------------------------
        filter_dropdowns(
            department_id="ove_department_selection",
            household_id="ove_farmer_selection",
            include_hh_db=False
        ),
        # -------------------------------------------------------------
        ui_row(
            ui_column(ui.card(ui.output_ui(id="dep_household_count"),), span=3),

            ui_column(
                ui.card(
                    ui_row(
                        ui_column(ui.output_ui(id="avg_pro_prod_input"), span=4),
                        ui_column(ui.output_ui(id="perform_irrigation_input"), span=4),
                        ui_column(ui.output_ui(id="source_water_input"), span=4)
                    )
                ), 
                span=9
            )
        ),

        ui.hr(),
        # -------------------------------------------------------------
        ui_row(
            ui_column(
                ui.card(ui.output_plot(id="irrigation_pactice_plot")),
                span=8
            ),
            ui_column(
                
                ui.card(ui.output_plot(id="crop_deparment_count_plot")),
                span=4
            ),
        ),
        # ----------------------------------------------------------------
        ui_row(
            ui_column(
                ui.card(ui.output_plot(id="share_roots_tuber_plot")),
                span=8
            ),
            ui_column(
                ui.card(
                    ui.div(
                        ui.h5("Household Irrigated Crops by Department", class_="mb-1"),
                        ui.output_data_frame(id="household_irrigated_crops"),
                        class_="table_irr_output"
                    )
                ),
                span=4
            )
        ),
        # ------------------------------------------------------------------

        ui.br(),
        # ----------------------------------------------------------
        ui.card(
            ui_row(
                ui_column(
                    ui.navset_pill(
                        ui.nav_panel("All", ui.output_plot(id="all_rainfall_values_plot")),
                        ui.nav_panel("Forecaset only", ui.output_plot(id="forecast_values_plot")),
                        ui.nav_panel("Historical only", ui.output_plot(id="history_values_plot")),
                        id="forecast_chart_options"
                    ),
                    span=9
                ),
                ui_column(
                    ui.output_ui("quntity_changes"),
                    span=3
                )
            ),
        ),
        
        ui.br()
    )





@module.server
def overview_server(input:Inputs, output:Outputs, session:Session, data_dict:dict):

    # Confirm Dashboard data ---------------------------------------------------------
    @reactive.Calc
    def db_data():
        req(data_dict)

        if not data_dict["error"]() and not data_dict["db_data"]()["error"]:
            return data_dict["db_data"]()["data"]
        
    @reactive.Calc
    def prod_nc():
        req(data_dict)

        if not data_dict["error"]() and not data_dict["prod_nc"]()["error"]:
            return data_dict["prod_nc"]()["data"]
        
    @reactive.Calc
    def rainfall_qty():
        req(data_dict)

        if not data_dict["error"]() and not data_dict["rainfall_qty"]()["error"]:
            return data_dict["rainfall_qty"]()["data"]


    # Update Overview department dropdown ------------------------
    @reactive.effect
    def _():
        req(db_data)
        dep_choice = get_unique_values_list(db_data(), "department")

        if not dep_choice["error"]:
            ui.update_select(
                "ove_department_selection",
                choices=dep_choice["value"],
                session=session
            )

    # Filter db_data by department -------------------------------
    @reactive.Calc
    def fdb_data():
        req(db_data, input.ove_department_selection)

        filt_df = filter_department(db_data(), input.ove_department_selection())
        if not filt_df["error"]:
            return filt_df["data"]
        else:
            return None
        
    # Household count --------------------------------------------
    @output(id="dep_household_count")
    @render.ui
    def _():
        req(fdb_data)
        count_value = count_household(fdb_data())
        if not count_value["error"]:
            return household_count_card(count_value["value"])
        
    # Number of processed products --------------------------------
    @output(id="avg_pro_prod_input")
    @render.ui
    def _():
        req(fdb_data)
        txt_output = calculate_avg_processed_product(fdb_data())
        if not txt_output["error"]:
            return metric_output("process_product", txt_output["value"])
        
    # Percentage of farmers that performed irrigation
    @output(id="perform_irrigation_input")
    @render.ui
    def _():
        req(fdb_data)
        txt_output = percent_perform_irrigation(fdb_data())
        if not txt_output["error"]:
            return metric_output("proportion_irrigation", txt_output["value"])

    # Most used source of water.
    @output(id="source_water_input")
    @render.ui
    def _():
        req(fdb_data)
        txt_output = most_used_source_water(fdb_data())
        if not txt_output["error"]:
            return metric_output("water_source", txt_output["value"], False)
    

    # ------------------------------------------------------------------
    @output(id="crop_deparment_count_plot")
    @render.plot
    def crop_deparment_count_plot():
        req(db_data, prod_nc)
        p_output = crop_department_count(db_data(), prod_nc())
        if not p_output["error"]:
            return p_output["plot"]

        
    @output(id="irrigation_pactice_plot")
    @render.plot
    def irrigation_pactice_plot():
        req(db_data, prod_nc)
        p_output = irrigation_practice_by_household(db_data())
        if not p_output["error"]:
            return p_output["plot"]
        
    @output(id="share_roots_tuber_plot")
    @render.plot
    def share_roots_tuber_plot():
        req(db_data, prod_nc)
        p_output = root_tubers_share(db_data())
        if not p_output["error"]:
            return p_output["plot"]


    @output(id="household_irrigated_crops")
    @render.data_frame
    def household_irrigated_crops():
        req(fdb_data, prod_nc)

        df_dict = households_use_irrigation_on_crops(fdb_data(), prod_nc())
        if not df_dict["error"]:
            return df_dict["data"]


    # Timeseries -------------------------------------------------------
    # Forecast:
    @reactive.Calc
    def forecast():
        req(rainfall_qty, input.ove_department_selection)

        forecast_dict = forecast_rainfall_monthly_quantity(
            rainfall_qty(), 
            input.ove_department_selection(),
            n_future_period=24
        )
        if not forecast_dict["error"]:
            forecast, orginal_cleaned_df, _ = forecast_dict["values"]
            all_records_dict = forecast_output(orginal_cleaned_df, forecast, "table")

            if not all_records_dict["error"]:
                return all_records_dict["data"]
                    
    # output:
    # All records:
    @output(id="all_rainfall_values_plot")
    @render.plot
    def all_rainfall_values_plot():
        req(forecast, input.ove_department_selection)
        p_output = create_forecast_plot(forecast(), input.ove_department_selection(), "all")
        if not p_output["error"]:
            
            return p_output["plot"]
    
    # Forecast:
    @output(id="forecast_values_plot")
    @render.plot
    def forecast_values_plot():
        req(forecast, input.ove_department_selection)
        p_output = create_forecast_plot(forecast(), input.ove_department_selection(), "forecast")
        if not p_output["error"]:
            return p_output["plot"]
    
    # History:
    @output(id="history_values_plot")
    @render.plot
    def history_values_plot():
        req(forecast, input.ove_department_selection)
        p_output = create_forecast_plot(forecast(), input.ove_department_selection(), "historical")
        if not p_output["error"]:
            return p_output["plot"]
    

    # Update MoM & YoY cards ------------------->
    @output(id="quntity_changes")
    @render.ui
    def _():
        req(forecast)
        mom_check = calculate_mom(forecast())
        yoy_check = calculate_yoy(forecast())

        if not mom_check["error"] and not yoy_check["error"]:
            return mom_yoy_card(
                round(mom_check["value"]), 
                round(yoy_check["value"], 2),
                mom_check["month_highest"],
                yoy_check["yr_highest_month"]
            )
            
                


        

        
    
            