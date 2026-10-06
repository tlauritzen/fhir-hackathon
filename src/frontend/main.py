from custom_sub_pages import custom_sub_pages, protected
from questionnaire_page import questionnaire_page

from daily_activity import daily_activity_page
from search_page import search_page

from nicegui import app, ui


@ui.page('/')
@ui.page('/{_:path}')
def main_page():
    def handle_logout():
        app.storage.user.clear()
        ui.navigate.reload()

    with ui.header().classes('items-center bg-blue-100') as header:
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Questionnaire', on_click=lambda: ui.navigate.to('/questionnaire')).props('flat')
        ui.button('Daily Activity', on_click=lambda: ui.navigate.to('/daily_activity')).props('flat')
        ui.button('Search', on_click=lambda: ui.navigate.to('/search_page')).props('flat')
        ui.button('Secret', on_click=lambda: ui.navigate.to('/secret')).props('flat')
        ui.button('Invalid', on_click=lambda: ui.navigate.to('/invalid')).props('flat')
        ui.button('Error', on_click=lambda: ui.navigate.to('/error')).props('flat')
        ui.space()
        if app.storage.user.get('patient_id'):
            ui.markdown(f"Patient ID: **{app.storage.user.get('patient_id', 'Unknown')}**").classes('text-gray-600')
            ui.button('Logout', icon='logout').props('flat').on_click(handle_logout)

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
