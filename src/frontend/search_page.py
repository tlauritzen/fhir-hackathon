from nicegui import ui

def search_page():
    ui.markdown("## Search")
    ui.markdown("Enter a query to search **FHIR** resources.")


if __name__ == "__main__":
    search_page()