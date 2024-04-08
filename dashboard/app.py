from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from pathlib import Path

from modules import mod_data_input, mod_overview


app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_spacer(),
    ui.nav_spacer(),
    ui.nav_spacer(),
    ui.nav_panel(
        "Data Import",
        mod_data_input.data_input_ui("page_data_input"),
        value="input_page"
    ),
    ui.nav_panel(
        "Overview",
        mod_overview.overview_ui("page_dashboard_overview"),
        value="overview_page"
    ), 
    ui.nav_spacer(),

    title="Dashboard Title",
    id="agric_main_nav_db",
    underline=True,
    bg="#64B6AC",
    
    header=ui.tags.head(
        # ui.tags.link(rel="stylesheet", href="style.css")
        ui.include_css(Path(__file__).parent / "www/style.css")
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    """ """

    db_data_dict = mod_data_input.data_input_server("page_data_input", "")

    mod_overview.overview_server("page_dashboard_overview", db_data_dict)



www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)