from shiny import ui
from faicons import icon_svg


def ui_row(*args, add_class:str=None):
    
    add_container_class = add_class if add_class is not None else ""
    return ui.div(
        *args,
        class_=f"grid {add_container_class}",
        style = "--bs-columns:12;",
    )

def ui_column(*args, span=6, add_class:str=None):

    add_container_class = add_class if add_class is not None else ""
    return ui.div(
        *args,
        # class_=f"cs_ui_row {add_container_class}"
        class_=f"g-col-12 g-col-md-12 g-col-lg-{span} {add_container_class}"
    )


def alert_container(alert_type:str, text:str):
    """ """
    if alert_type == "info":
        icon_name = "circle-info"
        add_class = "bg-primary"
        text_color = "text-white" # danger, secondary, warning, info, muted, white, dark
    elif alert_type == "danger":
        icon_name = "circle-exclamation"
        add_class = "bg-danger"
        text_color = "text-white"

    return ui.TagList(
        ui.div(
            icon_svg(name=icon_name, height="1.5rem", margin_left="0"),
            ui.p(text, class_="p-1 mt-1"),
            class_=f"{add_class} p-4 {text_color} rounded alert_container"
        )
    )



def filter_dropdowns(department_id:str, household_id:str, include_hh_db:bool=True):
    """ """
    if include_hh_db:
        household_db_tag = ui.TagList(
            ui.input_select(
                id=household_id, 
                label="Select Household ID",
                choices={"not_selected": "Not Selected"},
                width="50%"
            ),
        )
    else:
        household_db_tag = ui.TagList()

    return ui.TagList(
        ui.card(
            ui.layout_columns(
                ui.input_select(
                    id=department_id, 
                    label="Select Department",
                    choices={"not_selected": "Not Selected"},
                    width="50%"
                ),

                household_db_tag
            )
        )
    )