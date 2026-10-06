from collections.abc import Callable

from nicegui import app, ui
from nicegui.page_arguments import RouteMatch

from fhirpy import SyncFHIRClient


client = SyncFHIRClient("https://hapi.fhir.org/baseR4")


def protected(func: Callable) -> Callable:
    """Decorator to mark a route handler as requiring authentication for the custom_sub_pages."""
    func._is_protected = True  # pylint: disable=protected-access
    return func


class CustomSubPages(ui.sub_pages):
    """Custom ui.sub_pages with built-in authentication and custom 404 handling."""

    def _render_page(self, match: RouteMatch) -> bool:
        if self._is_route_protected(match.builder) and not self._is_authenticated():
            self._show_login_form(match.full_url)
            return True
        return super()._render_page(match)

    def _render_404(self) -> None:
        with ui.column().classes('absolute-center items-center'):
            ui.icon('error_outline', size='4rem').classes('text-red')
            ui.label('404 - Page Not Found').classes('text-2xl text-red')
            ui.label(f'The page "{self._router.current_path}" does not exist.').classes('text-gray-600')
            with ui.row().classes('mt-4'):
                ui.button('Go Home', icon='home', on_click=lambda: ui.navigate.to('/')).props('outline')
                ui.button('Go Back', icon='arrow_back', on_click=ui.navigate.back).props('outline')

    def _render_error(self, error: Exception) -> None:
        with ui.column().classes('absolute-center items-center'):
            ui.icon('error_outline', size='4rem').classes('text-red')
            ui.label('500 - Internal Server Error').classes('text-2xl text-red')
            ui.label(f'The page "{self._router.current_path}" produced an error.').classes('text-gray-600')
            # we do not recommend to show exception messages in production (security risk)
            ui.label(str(error)).classes('text-gray-600')
            with ui.row().classes('mt-4'):
                ui.button('Go Home', icon='home', on_click=lambda: ui.navigate.to('/')).props('outline')
                ui.button('Go Back', icon='arrow_back', on_click=ui.navigate.back).props('outline')

    def _is_route_protected(self, handler: Callable) -> bool:
        return getattr(handler, '_is_protected', False)

    def _is_authenticated(self) -> bool:
        return app.storage.user.get('patient_id', False)

    def _show_login_form(self, intended_path: str) -> None:
        with ui.card().classes('absolute-center items-stretch'):
            ui.label('Indtast patient').classes('text-2xl')
            ui.label('Indtast det fulde navn på den patient, som udfylder spørgeskemaet.')
            ui.label('Måske er det dig selv?')
            patient = ui.input('Patientens navn', password=False, password_toggle_button=False) \
                .classes('w-100').props('autofocus')

            def try_login():
                if patient.value:
                    try:
                        patient_obj = client.resources("Patient").search(name=patient.value).get()
                        app.storage.user["patient_id"] = patient_obj["id"]
                        self._reset_match()
                        ui.navigate.to(intended_path)
                        ui.navigate.reload()
                    except BaseException:
                        import traceback; traceback.print_exc()
                        ui.notify("NO GOOD, try LUCKMASTER", color="negative")
                else:
                    ui.notify('Incorrect passphrase', color='negative')

            patient.on('keydown.enter', try_login)
            ui.button('Fortsæt', on_click=try_login)


# Function-like access following NiceGUI convention where classes are callable to feel like functions
custom_sub_pages = CustomSubPages
