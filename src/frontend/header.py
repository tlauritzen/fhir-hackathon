from nicegui import ui, app
from nicegui import context

def SharedHeader(active_page: str = "Home"):
    with ui.header().classes('items-center bg-blue-100') as header:
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Questionnaire', on_click=lambda: ui.navigate.to('/questionnaire')).props('flat')
        ui.button('Daily Activity', on_click=lambda: ui.navigate.to('/daily_activity')).props('flat')
        ui.button('Search', on_click=lambda: ui.navigate.to('/search_page')).props('flat')
        ui.button('Secret', on_click=lambda: ui.navigate.to('/secret')).props('flat')
        ui.button('Invalid', on_click=lambda: ui.navigate.to('/invalid')).props('flat')
        ui.button('Error', on_click=lambda: ui.navigate.to('/error')).props('flat')
        ui.space()
        ui.button('Logout', icon='logout').props('flat') \
            .bind_visibility_from(app.storage.user, 'authenticated') \
            .on_click(lambda: app.storage.user.update(authenticated=False)) \
            .on_click(lambda: ui.navigate.to('/'))