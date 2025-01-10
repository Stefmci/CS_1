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
        User.list_users()

        if st.button("Anwendung neu laden"):
            st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)

    with tab2:
        User.add_user()

    with tab3:
        User.delete_user()

def geraeteverwaltung():
    st.title("Geräteverwaltung")
    tab1, tab2, tab3 = st.tabs(["Geräte anzeigen", "Gerät hinzufügen", "Gerät bearbeiten"])

    if "devices" not in st.session_state:
        st.session_state["devices"] = []

    if not st.session_state["devices"]:
        st.session_state["devices"] = Device.find_all()

    with tab1:
        st.header("Geräte anzeigen")
        if st.session_state["devices"]:
            for device in st.session_state["devices"]:
                st.write(f"ID: {device.device_name}, Verantwortlicher: {device.managed_by_user_id}")
        else:
            st.info("Es sind keine Geräte in der Datenbank gespeichert.")

        if st.button("Geräteliste neu laden"):
            st.session_state["devices"] = Device.find_all()
            st.rerun()

    with tab2:
        st.header("Gerät hinzufügen")
        device_name = st.text_input("Gerätename", key="add_device_name")
        managed_by_user_id = st.text_input("Verantwortlicher Benutzer (ID)", key="add_managed_by_user_id")

        if st.button("Gerät speichern"):
            if device_name and managed_by_user_id:
                new_device = Device(device_name=device_name, managed_by_user_id=managed_by_user_id)
                new_device.store_data()
                st.success(f"Gerät '{device_name}' wurde erfolgreich hinzugefügt!")

                st.session_state["devices"] = Device.find_all()
            else:
                st.error("Bitte sowohl Gerätename als auch Benutzer-ID ausfüllen.")

    with tab3:
        st.header("Gerät löschen")
        st.write("Wähle ein Gerät zum Löschen aus der Liste aus.")

        device_names = [device.device_name for device in st.session_state["devices"]]
        selected_device = st.selectbox("Gerät auswählen", ["---"] + device_names)

        if selected_device != "---":
            if st.button("Gerät löschen"):
                for device in st.session_state["devices"]:
                    if device.device_name == selected_device:
                        device.delete()  # Gerät aus der Datenbank löschen
                        st.success(f"Gerät '{selected_device}' wurde erfolgreich gelöscht!")
                        st.session_state["devices"] = Device.find_all()
                        break


        
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


