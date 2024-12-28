#Daten von: https://calendar-component.streamlit.app/

import pandas as pd

events = [
    {
        "title": "Reservierung Gerät 1",
        "start": "2023-12-01",
        "end": "2023-12-03",
        "backgroundColor": "#FF6C6C",
        "borderColor": "#FF6C6C",
    },
    {
        "title": "Reservierung Gerät 2",
        "start": "2023-12-05",
        "end": "2023-12-07",
        "backgroundColor": "#FFBD45",
        "borderColor": "#FFBD45",
    },
    {
        "title": "Reservierung Gerät 3",
        "start": "2023-12-10",
        "end": "2023-12-12",
        "backgroundColor": "#3DD56D",
        "borderColor": "#3DD56D",
    },
]

options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "start": "prev,next today",
        "center": "title",
        "end": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "editable": False,
}

#Tabelle auf Startseite
data = {
    "Gerät": ["CNC-Fräse", "Lötstation", "Laserschneider"],
    "bis einschließlich nicht verfügbar": ["25.01.2025", "30.01.2025", "22.01.2025"],
    "Bemerkung": ["Wartungsarbeiten", "Wartungsarbeiten", "Wartungsarbeiten"],
}

df = pd.DataFrame(data)