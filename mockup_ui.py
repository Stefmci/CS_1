import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import general_data as bu
import ui_device as ui
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

    # Anzeige der Benutzerliste
    st.header("Nutzerliste:")
    try:
        users = User.find_all()
        if users:
            st.dataframe(
                [{"ID": user.id, "Name": user.name} for user in users],
                use_container_width=True
            )
        else:
            st.info("Keine Benutzer gefunden.")
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Benutzerliste: {e}")

    # Benutzer hinzufügen
    st.header("Nutzer hinzufügen")
    user_id = st.text_input("Benutzer-ID")
    user_name = st.text_input("Benutzername")
    if st.button("Benutzer speichern"):
        if user_id and user_name:
            try:
                user = User(user_id, user_name)
                existing_user = User.find_by_attribute("id", user_id)
                if existing_user:
                    st.warning(f"Benutzer mit ID {user_id} existiert bereits. Er wird aktualisiert.")
                user.store_data()
                st.success(f"Benutzer {user_name} (ID: {user_id}) wurde hinzugefügt/aktualisiert!")
                st.experimental_rerun()  # Seite aktualisieren
            except Exception as e:
                st.error(f"Fehler beim Speichern des Benutzers: {e}")
        else:
            st.error("Bitte sowohl eine ID als auch einen Namen eingeben.")

    # Benutzer löschen
    st.header("Benutzer löschen")
    del_user_id = st.text_input("ID des zu löschenden Benutzers")
    if st.button("Benutzer löschen"):
        if del_user_id:
            try:
                user = User(del_user_id, "")
                if not User.find_by_attribute("id", del_user_id):
                    st.warning(f"Benutzer mit ID {del_user_id} wurde nicht gefunden.")
                else:
                    user.delete()
                    st.success(f"Benutzer mit ID {del_user_id} wurde gelöscht!")
                    st.experimental_rerun()  # Seite aktualisieren
            except Exception as e:
                st.error(f"Fehler beim Löschen des Benutzers: {e}")
        else:
            st.error("Bitte eine Benutzer-ID eingeben.")


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
                st.write(f"ID: {device['ID']}, Name: {device['Name']}, Verantwortlicher: {device['Verantwortlicher']}")
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


