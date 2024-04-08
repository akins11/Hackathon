from faicons import icon_svg
from shiny import ui
import calendar

from components.comp_global import ui_row, ui_column

style_wide = "display: flex; justify-content: flex-start; align-items: flex-end; gap: 2rem;"

def household_count_card(value:int):
    """ """
    return ui.TagList(
        ui.div(
            ui.p("Number of households", class_="fs-5 fw-bold text-muted househ_card_title"), 
            ui.p(value, class_="fs-2 text-black househ_card_value"),
            class_="househ_card",
        )
    )


def metrics_card():
    """ """
    main_tag = ui.TagList()
    ids = ["avg_pro_prod_input", "perform_irrigation_input", "source_water_input"]
    descriptions = [
        "Average number of process products",
        "Proportion performing irrigation",
        "Most used source of water"
    ]
    for id, desc in zip(ids, descriptions):
        tag = ui_column(
                ui.div(
                ui.p(desc, class_="fs-5 fw-normal text-muted"),
                ui.p(ui.output_ui(id=id), class_="fs-2 fw-bold text-black"),
                class_="d-flex align-items-center gap-5 p-1",
            ),
             span=4
        )
        main_tag.append(tag)

    return ui.TagList(
        ui.div(
            ui_row(main_tag),
            class_="d-flex justify-content-between",
            style="height: 5rem !important; width: 90%;"
        )
    )

def metric_output(metric:str, value:str, inclued_border:str=True):
    """ """
    border = "bdr" if inclued_border else ""
    if metric == "process_product":
        desc  = "Average number of processed products"
    
    elif metric == "proportion_irrigation":
        desc = "Proportion performing irrigation"
        value = f"{value}%"
    else:
        desc = "Most used source of water"


    return ui.div(
        ui.p(desc, class_="fs-5 fw-normal text-muted metric_card_desc"),
        ui.p(value, class_="fs-3 text-black metric_card_value"),
        class_=f"metric_card {border}"
    ),



def mom_yoy_card(
        mom_value:float, 
        yoy_value:float, 
        mom_highest_month:int,
        highest_year:int
):
    """ """
    
    current_month = mom_highest_month
    previous_month = mom_highest_month - 1

    abbr_list = list(calendar.month_abbr)[1:]
    previous_month = abbr_list[previous_month]
    current_month = abbr_list[current_month]

    return ui.div(
        ui.div(
            ui.p("MoM", class_="fs-5 fw-normal mb-1"),
            ui.div(
                ui.p(f"{previous_month}/{current_month}", class_="fs-4 fw-normal"), 
                ui.p(ui.span(f"{mom_value} %", class_="fs-2 fw-normal"), class_="fs-4 fw-normal mb-4"), 
                class_="my_card_child__row"
            ),
            class_="my_card_child"
        ),
        ui.div(
            ui.p("YoY", class_="fs-5 fw-normal mb-1"),
            ui.div(
                ui.p(f"22/23 {abbr_list[highest_year]}", class_="fs-4 fw-normal"), 
                ui.p(ui.span(f"{yoy_value} %", class_="fs-2 fw-normal"), class_="fs-4 fw-normal mb-4"), 
                class_="my_card_child__row"
            ),
            class_="my_card_child"
        ),
        class_="my_card bg-success"
    )


