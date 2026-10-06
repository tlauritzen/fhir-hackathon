from nicegui import ui, app

def SharedHeader(active_page: str = ""):
    with ui.header().classes('items-center bg-blue-100') as header:
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Questionnaire', on_click=lambda: ui.navigate.to('/questionnaire')).props('flat')
        ui.button('Secret', on_click=lambda: ui.navigate.to('/secret')).props('flat')
        ui.button('Invalid', on_click=lambda: ui.navigate.to('/invalid')).props('flat')
        ui.button('Error', on_click=lambda: ui.navigate.to('/error')).props('flat')
        ui.space()
        ui.button('Logout', icon='logout').props('flat') \
            .bind_visibility_from(app.storage.user, 'authenticated') \
            .on_click(lambda: app.storage.user.update(authenticated=False)) \
            .on_click(lambda: ui.navigate.to('/'))
    for button in header.default_slot.children:
        if isinstance(button, ui.button) and button.text == active_page:
            button.props('flat color=red-500 text-white font-bold')