import streamlit as st
from streamlit_calendar import calendar   
import userinterface as ui


st.sidebar.title("Navigation")
auswahl = st.sidebar.radio("Seite auswählen", ["Startseite", "Reservierung", "Benutzerverwaltung", "Geräteverwaltung", "Wartungs-Management"])

if auswahl == "Reservierung":
    ui.Reservierung()
elif auswahl == "Benutzerverwaltung":
    ui.benutzerverwaltung()
elif auswahl == "Geräteverwaltung":
    ui.geraeteverwaltung()
elif auswahl == "Wartungs-Management":
    ui.geraetewartung()
elif auswahl == "Startseite":
    ui.startseite()
