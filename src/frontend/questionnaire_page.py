from nicegui import app, ui
from custom_sub_pages import custom_sub_pages, protected
from fhirpy import AsyncFHIRClient

def get_question_artifact():
    print("grab question")
    client = AsyncFHIRClient("https://hapi.fhir.org/baseR4")

def get_question():
    pass

def get_choices():
    pass

def submit_answer():
    pass


placeholder_question = {
    "question": "Er du ok?",
    "choices": {
        "awdhwakdhdkwahdwaa-awdwadwad-dwawadwad1": "Ja",
        "awdhwakdhdkwahdwaa-awdwadwad-dwawadwad2": "Nej",
        "awdhwakdhdkwahdwaa-awdwadwad-dwawadwad3": "Ved ikke",
    },
}

questions = [placeholder_question]

def question(question: dict):
    ui.markdown(f"## {question["question"]}")
    ui.radio(question["choices"])

@protected
def questionnaire_page():
    get_question_artifact()
    with ui.column().classes('flex-grow p-4'):
        ui.markdown('''# Spørgeskema

Dette spørgeskema skal udfyldes hver anden uge.
                    
Det er vigtigt, at du svarer ærligt, da dine svar vil hjælpe os med at forstå din situation bedre og give dig den bedst mulige behandling.''')
        for q in questions:
            question(q)

if __name__ == "__main__":
    questionnaire_page()