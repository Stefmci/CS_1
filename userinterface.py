import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import general_data as bu


def startseite():
    st.title("Willkommen ")
    st.header("bei der Geräteverwaltung der Hochschule")
    st.write("Am linken Rand befindet sich die Navigation, wo Sie zwischen den verschiedenen Seiten wechseln können.")
    st.divider()
    st.title("News")
    st.write("Nächste Woche findet die Einschlung der CNC-Fräse statt.")
    st.divider()
    st.title("Wartungsarbeiten")
    st.write("Folgende Geräte sind nicht verfügbar.")
    st.table(bu.df_startseite)
    st.divider()
    st.write("Bei Fragen oder Problemen wenden Sie sich bitte an den Administrator.")
    
def Reservierung():
    st.title("Reservierung")
    st.selectbox("Gerät auswählen", ["Laserschneider", "3D-Drucker", "CNC-Fräse", "Schweißgerät", "Lötkolben", "Oszilloskop", "Multimeter", "Netzteil", "Funktionsgenerator"])
    st.selectbox("Wähle ein Datum:", generate_next_two_weeks())
    st.button("Gerät reservieren")
    st.header("Übersicht der Reservierungen")
    calendar(events=bu.events, options=bu.options, key="static_calendar")
    
def benutzerverwaltung():
    st.title("Nutzerverwaltung")
    st.header("Nutzerliste:")
    st.table(bu.df_nutzer)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Benutzer ändern")
    with col2:
        st.button("Benutzer löschen")
    st.header("Nutzer hinzufügen")
    user_name = st.text_input("Benutzername")
    user_email = st.text_input("E-Mail Adresse")
    if st.button("Benutzer speichern"):
        st.success(f"Benutzer {user_name} mit e-mail {user_email} wurde hinzugefügt!")

def geraeteverwaltung():
    st.title("Geräteverwaltung")
    st.header("Gerät hinzufügen")
    device_id = st.text_input("Geräte-ID")
    device_name = st.text_input("Gerätename")
    if st.button("Gerät speichern"):
        st.success(f"Gerät {device_name} mit ID {device_id} wurde hinzugefügt!")
        
def geraetewartung():
    st.title("Wartungs-Management")
    st.header("Wartungsplan")
    calendar(events=bu.events, options=bu.options, key="static_calendar")
    st.header("Wartungsliste")
    st.table(bu.df_wartung)
    st.button("Anpassen")
    st.header("Gerät hinzufügen")
    device_id = st.text_input("Geräte-ID")
    device_name = st.text_input("Gerätename")
    if st.button("Gerät speichern"):
        st.success(f"Gerät {device_name} mit ID {device_id} wurde hinzugefügt!")
        
def generate_next_two_weeks():
    today = datetime.today()
    next_two_weeks = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(14)]
    return next_two_weeks


