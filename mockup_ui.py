import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import general_data as bu
from devices import Device
import users as User


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
    tab1, tab2, tab3 = st.tabs(["Nutzerliste", "Nutzer hinzufügen", "Nutzer löschen"])
    
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Nutzerliste"

    with tab1:
        User.list_users()  # Funktion zum Anzeigen der Nutzerliste

        # Button hinzufügen, um die Anwendung neu zu laden
        if st.button("Anwendung neu laden"):
            st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)

    with tab2:
        User.add_user()  # Funktion zum Hinzufügen von Nutzern

    with tab3:
        User.delete_user()  # Funktion zum Löschen von Nutzern



def geraeteverwaltung():
    st.title("Geräteverwaltung")

    # Session State initialisieren
    if "devices" not in st.session_state:
        st.session_state["devices"] = []  # Liste der Geräte aus der Datenbank

    # Datenbank-Verbindung initialisieren und Geräte aus der Datenbank laden
    st.session_state["devices"] = Device.find_all()

    # Dropdown-Menü für Aktionen
    option = st.selectbox(
        "Wähle eine Aktion",
        ["Gerät hinzufügen", "Geräte anzeigen", "Gerät bearbeiten"]
    )

    # Gerät hinzufügen
    if option == "Gerät hinzufügen":
        st.header("Gerät hinzufügen")
        device_name = st.text_input("Gerätename", key="add_device_name")
        managed_by_user_id = st.text_input("Verantwortlicher Benutzer (ID)", key="add_managed_by_user_id")

        if st.button("Gerät speichern"):
            if device_name and managed_by_user_id:
                # Neues Gerät erstellen
                new_device = Device(device_name=device_name, managed_by_user_id=managed_by_user_id)
                
                # Gerät in die Datenbank speichern
                new_device.store_data()

                st.success(f"Gerät '{device_name}' wurde in der Datenbank gespeichert!")
            else:
                st.error("Bitte sowohl Gerätename als auch Benutzer-ID ausfüllen.")

    # Geräte anzeigen
    elif option == "Geräte anzeigen":
        st.header("Geräte anzeigen")
        if st.session_state["devices"]:
            # Alle gespeicherten Geräte aus der Datenbank anzeigen
            for device in st.session_state["devices"]:
                st.write(f"ID: {device.device_name}, Verantwortlicher: {device.managed_by_user_id}")
        else:
            st.info("Es sind keine Geräte in der Datenbank gespeichert.")

    elif option == "Gerät bearbeiten":
        st.header("Gerät bearbeiten")
        st.write("Hier kannst du ein vorhandenes Gerät bearbeiten.")
        # Beispiel für Bearbeitungslogik
        device_name = st.text_input("Gerätename zum Bearbeiten")
        if st.button("Gerät bearbeiten"):
            st.info(f"Gerät mit Name {device_name} wurde zur Bearbeitung geöffnet.")

        
def geraetewartung():
    st.title("Wartungs-Management")
    st.header("Wartungsplan")
    calendar(events=bu.events, options=bu.options, key="static_calendar")
    st.header("Wartungsliste")
    st.table(bu.df_wartung)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Anpassen")
    with col2:
        st.button("Löschen")
    st.header("Gerät hinzufügen")
    device_id = st.text_input("Geräte-ID")
    device_name = st.text_input("Gerätename")
    if st.button("Gerät speichern"):
        st.success(f"Gerät {device_name} mit ID {device_id} wurde hinzugefügt!")
        
def generate_next_two_weeks():
    today = datetime.today()
    next_two_weeks = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(14)]
    return next_two_weeks


