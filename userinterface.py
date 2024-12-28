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

    # Session State initialisieren
    if "devices" not in st.session_state:
        st.session_state["devices"] = []  # Liste der Geräte

    st.title("Geräteverwaltung")

    # Dropdown-Menü für Aktionen
    option = st.selectbox(
        "Wähle eine Aktion",
        ["Gerät hinzufügen", "Geräte anzeigen", "Gerät bearbeiten"]
    )

    # Gerät hinzufügen
    if option == "Gerät hinzufügen":
        st.header("Gerät hinzufügen")
        device_id = st.text_input("Geräte-ID", key="add_device_id")
        device_name = st.text_input("Gerätename", key="add_device_name")

        if st.button("Gerät speichern"):
            if device_id and device_name:
                # Gerät zur Session State-Liste hinzufügen
                st.session_state["devices"].append({"ID": device_id, "Name": device_name})
                st.success(f"Gerät '{device_name}' mit ID '{device_id}' wurde hinzugefügt!")
            else:
                st.error("Bitte sowohl Geräte-ID als auch Gerätename ausfüllen.")

    # Geräte anzeigen
    elif option == "Geräte anzeigen":
        st.header("Geräte anzeigen")
        if st.session_state["devices"]:
            # Alle gespeicherten Geräte auflisten
            for device in st.session_state["devices"]:
                st.write(f"ID: {device['ID']}, Name: {device['Name']}")
        else:
            st.info("Es sind keine Geräte vorhanden.")

    
    elif option == "Gerät bearbeiten":
        st.header("Gerät bearbeiten")
        st.write("Hier kannst du ein vorhandenes Gerät bearbeiten.")
        # Beispiel für Bearbeitungslogik
        device_id = st.text_input("Geräte-ID zum Bearbeiten")
        if st.button("Gerät bearbeiten"):
            st.info(f"Gerät mit ID {device_id} wurde zur Bearbeitung geöffnet.")
        
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


