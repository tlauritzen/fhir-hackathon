from nicegui import ui

AKTIVITETER = {
    "129006008": "Gang",
    "418060005": "Løb",
    "129016000": "Trappegang",
    "61686008": "Træning",
    "14468000": "Sport",
    "4751000": "Fritidsaktivitet (f.eks. cykling)",
}


def daily_activity_page():
    ui.label("Dagens målinger").classes("text-2xl")

    dato = ui.date()
    aktivitet = ui.select(AKTIVITETER, label="Type aktivitet").classes("w-64")
    minutter = ui.number("Antal minutter", min=0, step=5).classes("w-64")
    soevn = ui.number("Antal timers søvn", min=0, max=24, step=0.5).classes("w-64")

    def gem():
        if not dato.value or not aktivitet.value or minutter.value is None or soevn.value is None:
            ui.notify("Udfyld alle felter", color="negative")
            return
        maaling = {
            "dato": dato.value,
            "aktivitet_kode": aktivitet.value,
            "aktivitet_navn": AKTIVITETER[aktivitet.value],
            "minutter": int(minutter.value),
            "soevn_timer": soevn.value,
        }
        print(maaling)
        ui.notify(f"Gemt: {maaling['aktivitet_navn']} {maaling['minutter']} min, "
                  f"{maaling['soevn_timer']} timers søvn", color="positive")

    ui.button("Gem", on_click=gem)