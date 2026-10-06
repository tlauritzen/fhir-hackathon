from nicegui import app, ui
from header import SharedHeader

def question(question_text: str, choices: dict):
    ui.markdown('''
        ### Questionnaire 📝

        This is a questionnaire page for users to fill out.
    ''')
    ui.label(question_text)
    ui.radio(choices)

def questionnaire_page():
    with ui.column().classes('flex-grow p-4'):
        ui.label("Spørgeskema")
        ui.html("<p>Dette spørgeskema skal udfyldes hver anden uge.</p>")
        test_q = "Hvilken af følgende muligheder beskriver bedst din nuværende situation?"
        test_choices = {
            "Jeg har det godt og oplever ingen problemer.": "good",
            "Jeg har nogle mindre problemer, men det påvirker ikke min dagligdag væsentligt.": "minor",
            "Jeg har moderate problemer, som påvirker min dagligdag i nogen grad.": "moderate",
        }
        question(test_q, test_choices)

if __name__ == "__main__":
    questionnaire_page()