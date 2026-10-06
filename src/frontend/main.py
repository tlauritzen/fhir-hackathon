from custom_sub_pages import custom_sub_pages, protected
from questionnaire_page import questionnaire_page
from header import SharedHeader

from daily_activity import daily_activity_page
from search_page import search_page

from nicegui import app, ui


@ui.page('/')
@ui.page('/{_:path}')
def main_page():
    SharedHeader()

    custom_sub_pages({
        '/': home,
        '/secret': secret,
        '/error': error,
        '/questionnaire': questionnaire_page,
        '/daily_activity': daily_activity_page,
        '/search_page': search_page,
    }).classes('flex-grow p-4')


def home():
    ui.markdown('''
        This example shows inheritance from `ui.sub_pages` for decorator-based route protection and a custom 404 page.

        **Try it:** Navigate to "Secret" (passphrase: "spa") or "Invalid" for 404.
    ''')


def error():
    raise ValueError('some error message')


@protected
def secret():
    ui.markdown('''
        ### Secret Area 🔑

        This is confidential information only for authenticated users.
    ''')



if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        storage_secret="demo_secret_key_change_in_production",
        title="FHIR Track 2 Case Questionaire",
        native=False,
        reload=True,
        )
