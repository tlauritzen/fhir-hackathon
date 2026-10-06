from nicegui import ui
from daily_activity import AKTIVITETER

from fhirpy import SyncFHIRClient

def search_page():
    ui.markdown("## Search")
    ui.markdown("Enter a query to search **FHIR** resources.")

    ui.label("Search").classes("text-2xl")

    activity = ui.select(AKTIVITETER, label="Activity").classes("w-64")
    sleep = ui.checkbox(text="Sleep", value=True)

    patientName = "nhanes-112200"

    def search():
        endpoint = "https://hapi.fhir.org/baseR4"

        client = SyncFHIRClient(endpoint)

        resources = client.resources('Observation')  # Return lazy search set
        resources = resources.search(subject=patientName).limit(10)
        observations = resources.fetch()  # Returns list of AsyncFHIRResource
        print(observations)
        if sleep.value:
            print("Sleep active!")

        ui.notify(f"{sleep.value} {activity.value}", color="positive")

    ui.button("Search", on_click=search)


if __name__ == "__main__":
    search_page()