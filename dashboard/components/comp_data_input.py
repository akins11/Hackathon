from shiny import ui
from faicons import icon_svg

from components.comp_global import ui_row, ui_column

crop_type = ["Cocoa", "Cotton", "Yam", "Cassava"]


def create_fields_layout(
        input_ui, 
        output_field_id:str, 
        inclued_line_brake:bool=True,
        info_message:str="@@@@@"
):
    """ """

    if inclued_line_brake:
        br_tag = ui.br()
    else:
        br_tag = None

    return ui.TagList(
        ui_row(
            ui_column(input_ui, span=8),
            ui_column(ui.output_ui(id=f"{output_field_id}_check"), span=2),
            ui_column(
                ui.popover(
                    ui.input_action_link(
                        id=f"{output_field_id}_info_trigger",
                        label="",
                        icon=icon_svg("info", height="1rem", margin_left="0", margin_right="0")
                    ),
                    info_message,
                    id=f"{output_field_id}_info"
                ),
                span=2,
                add_class="mt-4"
            )
        ),

        br_tag
    )

def field_column(field_title:str, *args):
    """ 
    """
    return ui.TagList(
        ui.div(
            ui.h3(f"Post-{field_title} Data Fields", class_="field_title"),
            ui.br(),
            *args,
            class_="ip_pp_column"
        )

    )

def check_icon(okay:bool):

    if okay:
        icon_name = "circle-check"
        color_indicator = "#43CD80" # "text-success"
    else:
        icon_name = "circle-xmark"
        color_indicator = "#EE3B3B" #"text-danger"

    return ui.TagList(
        ui.div(
            icon_svg(
                name=icon_name, 
                fill=color_indicator,
                height="1.5rem", 
                margin_left="0", 
                margin_right="0"
            ),
            class_="d-flex justify-content-center align-items-center mt-3",
            style="width: 5rem; height: 3rem"
        )
    )


def data_collection_ui(send_data_id:str, check_append_id:str):
    """ 
    """

    return ui.TagList(
        ui.br(),
        ui.hr(),

        ui_row(
            ui_column(
                ui.input_task_button(
                    id=send_data_id,
                    label="Send Data"
                ),
                span=4
            ),
            ui_column(
                ui.output_ui(id=check_append_id),
                span=8
            )
        )
    )


def input_fields_ui():
    """ """
    return ui.layout_columns(
        field_column(
            "Planting",
            create_fields_layout(
                ui.input_text(
                    id="location_input_data",
                    label="Household location",
                    placeholder="Department ...",
                    width="100%"
                ),
                "location_input_add_ui",
                info_message="Based on your/the department"
            ),
            create_fields_layout(
                ui.input_selectize(
                    id="crop_data_input",
                    label="Select type of crop planted",
                    choices=crop_type,
                    multiple=True, width="100%"
                ),
                "select_crop_data_input_add_ui",
                info_message="Only grown crops"
            ),
            create_fields_layout(
                ui.input_numeric(
                    id="area_data_input",
                    label="Area cultivated (acres)",
                    value=1,
                    min=5, max=5000, step=10,
                    width="100%"
                ),
                "area_data_input_add_ui",
                info_message="Only cultivated area"
            ),
            create_fields_layout(
                ui.input_numeric(
                    id="qty_seed_data_input",
                    label="Quantity of seeds planted (Kg)",
                    value=1,
                    min=5, max=5000, step=10,
                    width="100%"
                ),
                "qty_seed_data_input_add_ui",
                info_message="During Agric season"
            ),
            create_fields_layout(
                ui.input_numeric(
                    id="qty_avg_rainfall_data_input",
                    label="Average rainfall quantity",
                    value=1,
                    min=5, max=5000, step=10,
                    width="100%"
                ),
                "qty_avg_rainfall_data_input_add_ui",
                info_message="Based on your area"
            ),
            create_fields_layout(
                ui.input_numeric(
                    id="avg_temperature_data_input",
                    label="Average temperature",
                    value=1,
                    min=5, max=5000, step=10,
                    width="100%"
                ),
                "avg_temperature_data_input_add_ui",
                info_message="Wthin farm area."
            ),
            create_fields_layout(
                ui.input_radio_buttons(
                    id="used_fertilizer",
                    label="Used fertilizer?",
                    choices={"Yes": True, "No": False},
                    selected=None,
                    width="100%"
                ),
                "used_fertilizer_add_ui",
                info_message="Did you use any kind of fertilizer?"
            ),
        ),

        # Post-harvest ------------------------------------->
        field_column(
            "Harvest",

                create_fields_layout(
                ui.input_selectize(
                    id="type_crop_harvest_input",
                    label="Select type of crop harvested",
                    choices=crop_type,
                    multiple=True, width="100%"
                ),
                "crop_data_input_add_ui",
                info_message="After planting season"
            ),
            create_fields_layout(
                ui.input_numeric(
                    id="qty_havst_data_input",
                    label="Qauntity harvested? (Kg)",
                    value=1, min=0, max=5000, step=10,
                    width="100%"
                ),
                "qty_havst_data_input_add_ui",
                info_message="After planting season"
            ),
            create_fields_layout(
                ui.input_numeric(
                    id="qty_consumed_data_input",
                    label="The qauntity consumed?",
                    value=1, min=0, max=5000, step=10,
                    width="100%"
                ),
                "qty_consumed_data_input_add_ui",
                info_message="After during season"
            ),
            create_fields_layout(
                    ui.input_numeric(
                        id="qty_sold_data_input",
                        label="The qauntity sold?",
                        value=1, max=5000, step=10,
                        width="100%"
                    ),
                "qty_sold_data_input_add_ui",
                info_message="After planting season"
            ),
            create_fields_layout(
                ui.input_selectize(
                    id="neg_impact_data_input",
                    label="What negative event happened during the agric season?",
                    choices=[
                        " ", "Flood", "Drought", "Diseases", "Soil Quality"
                    ],
                    selected=None,
                    width="100%"
                ),
                "neg_impact_data_input_add_ui",
                info_message="Optional"
            ),
        ),
    )