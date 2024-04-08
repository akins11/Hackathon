from shiny import Inputs, Outputs, Session, module, render, ui, reactive, req
import shinyswatch
from faicons import icon_svg

from components.comp_data_input import data_collection_ui, input_fields_ui
from components.comp_global import filter_dropdowns, alert_container

from logic.func_ui_data_input import (
    check_accurate_numeric_range, 
    check_accurate_new_data
)
from logic.func_save_read_db_tables import read_data_from_database
from logic.func_data_input import get_unique_values_list



crop_type = ["Cocoa", "Cotton", "Yam", "Cassava"]
db_path = "../aacc/dashboard/db/dash_db.duckdb"
 

@module.ui
def data_input_ui():

    return ui.TagList(
        shinyswatch.theme.minty(),

        ui.input_task_button("upload_db_data", "Update Dashboard Data"),

        ui.br(), ui.br(),

        filter_dropdowns(
            department_id="department_selection",
            household_id="household_selection",
            include_hh_db=True
        ),

        ui.navset_card_pill(
            ui.nav_panel(
                "Input Data Manually",
                ui.output_ui(id="manual_input_new_data_ui")
            ),

            ui.nav_panel(
                "Upload Data File Directly",
                ui.output_ui(id="upload_new_data_ui")
            )
        ),
        ui.br()
    )



@module.server
def data_input_server(input:Inputs, output:Outputs, session:Session, temp:dict):
    # Read in data from database ------------------------------------------------
    @reactive.Calc
    @reactive.event(input.upload_db_data)
    def db_data_dict():
        try:
            irg_data = read_data_from_database(db_path, "irrigation")
            return {"error": False, "data": irg_data}
        except ValueError as e:
            print(e)
            return {"error": True, "data": None}

    @reactive.Calc
    @reactive.event(input.upload_db_data)
    def prod_cn_dict():
        try:
            product_cn = read_data_from_database(db_path, "prod_code_name")
            return {"error": False, "data": product_cn}
        except ValueError as e:
            print(e)
            return {"error": True, "data": None}
    
    @reactive.Calc
    @reactive.event(input.upload_db_data)
    def rainfall_qty():
        try:
            rainfall = read_data_from_database(db_path, "rainfall_qty")
            return {"error": False, "data": rainfall}
        except ValueError as e:
            print(e)
            return {"error": True, "data": None}


    # Update Department & household dropdowns values ---------------------------------
    @reactive.effect
    def _():
        req(db_data_dict)
        if not db_data_dict()["error"]:
            dep_choice = get_unique_values_list(db_data_dict()["data"], "department")

            if not dep_choice["error"]:
                ui.update_select(
                    "department_selection",
                    choices=dep_choice["value"],
                    session=session
                )
            
    @reactive.effect
    def _():
        req(input.department_selection, db_data_dict)
        
        if not db_data_dict()["error"]:
            hus_choice = get_unique_values_list(
                db_data_dict()["data"], 
                "household_id",
                "department",
                input.department_selection()
            )
            if not hus_choice["error"]:
                ui.update_select(
                    "household_selection",
                    choices=hus_choice["value"],
                    session=session
                )


    # UI ------------------------------------------------------------------------------
    # Add manual data input ui 
    @output(id="manual_input_new_data_ui")
    @render.ui
    def _():
        req(input.department_selection, input.household_selection)

        if (input.department_selection() != "not_selected" and input.department_selection() is not None) and (input.household_selection() != "not_selected" and input.household_selection() is not None):
            return  ui.TagList(
                        input_fields_ui(),

                        data_collection_ui(
                            send_data_id="send_manually_inputed_farmers_data",
                            check_append_id="check_manually_inputed_new_data_append"
                        )
                    )
        else:
            return ui.TagList(
                alert_container(
                    "info",
                        """ 
                        Ensure the data you input is accurate, complete, and up-to-date. inaccurate
                        or outdated data can lead to incorrect analysis and decisons. Also input data
                        that is relevant to the analysis or visualization you intend to perform in the
                        dashboard and make sure your data is correctly formated before inputting it into
                        the dashboard. Ensure consistency in data types, naming conventions and structure
                        to facilitate accurate analysis.
                        """ 
                    )
                )


    # Add upload new data ui
    @output(id="upload_new_data_ui")
    @render.ui
    def _():
        req(input.department_selection, input.household_selection)

        if (input.department_selection() != "not_selected" and input.department_selection() is not None) and (input.household_selection() != "not_selected" and input.household_selection() is not None):
            return ui.TagList(
                    ui.input_file(
                        id="upload_farmer_new_data",
                        label="Upload new data"
                    ),

                    ui.br(),
                    ui.br(),
                    ui.output_ui(id="upload_notification"),

                    data_collection_ui(
                        send_data_id="send_uploaded_farmers_data",
                        check_append_id="check_uploaded_new_data_append"
                    )
                )
        else:
            return ui.TagList(
                alert_container(
                    "info",
                        """ 
                        Before importing data, make sure it is properly formatted and saved in an
                        acceptable file format such as CSV, Excel. check for any inconsistencies
                        missing values, or errors that could affect the analysis. After importing
                        the data validate that it has been imported correctly. check for any discrepancies
                        or issues that may have occurred during the import process and make sure to seek assistance
                        if needed.
                        """ 
                )
            )


    # Post-Planting Check ------------------------------------------------------------>
    @output(id="area_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.area_data_input())
        
    @output(id="qty_seed_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.qty_seed_data_input())
    
    @output(id="area_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.area_data_input())
    
    @output(id="qty_avg_rainfall_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.qty_avg_rainfall_data_input())
    
    @output(id="avg_temperature_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.avg_temperature_data_input())
    

    
    # Post-Planting Check ----------------------------------------->
    @output(id="qty_havst_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.qty_havst_data_input())
    
    @output(id="qty_consumed_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.qty_consumed_data_input())
    
    @output(id="qty_sold_data_input_add_ui_check")
    @render.ui
    def _():
        return check_accurate_numeric_range(input.qty_sold_data_input())
    

    @output(id="check_manually_inputed_new_data_append")
    @render.ui
    def _():
        req(input.send_manually_inputed_farmers_data)
        if input.send_manually_inputed_farmers_data():
            return check_accurate_new_data(True)
    

    # Check manually inputed data -----------------------------------
    # check before appending
    # check_manually_inputed_new_data_append
    # Data Logic  -------------------------------------------------->
    # .....
    # Output ----------------------------------------------------------------------------------->
    # @reactive.Calc
    def check_accurate_data():
        req(db_data_dict, prod_cn_dict)
        if not db_data_dict()["error"] and not prod_cn_dict()["error"] and not rainfall_qty()["error"]:
            return False
        else:
            return True
        # .....

    return {
        "error": check_accurate_data, 
        "db_data": db_data_dict,  
        "prod_nc": prod_cn_dict,
        "rainfall_qty": rainfall_qty
    }
