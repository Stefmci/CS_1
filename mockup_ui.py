import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import general_data as bu
from devices_inheritance import Device
from users_inheritance import User
import reservations as r
import reservation_service as rs
import pandas as pd



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
    st.title("Gerätereservierung")

    devices = [device.id for device in Device.find_all()]
    
    if not devices:
        st.warning("Es sind derzeit keine Geräte verfügbar.")
        return
    
    selected_device_name = st.selectbox("Gerät auswählen", devices, key="selected_device")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Startdatum", min_value=datetime.today(), key="start_date")
    with col2:
        end_date = st.date_input("Enddatum", min_value=start_date, key="end_date")

    users = [user.id for user in User.find_all()]
    selected_user = st.selectbox("Benutzer auswählen", users, key="selected_user")

    if st.button("Gerät reservieren"):
        if start_date and end_date and selected_device_name and selected_user:
            selected_device = Device.find_by_attribute("device_name", selected_device_name)
            
            if selected_device:
                success = selected_device.create_reservation(start_date, end_date)
                
                if success:
                    st.success(f"Reservierung für {selected_device_name} von {start_date} bis {end_date} wurde erfolgreich erstellt.")
                    st.rerun()
                else:
                    st.error("Reservierung nicht möglich: Der Zeitraum überschneidet sich mit einer bestehenden Reservierung.")
            else:
                st.error("Gerät nicht gefunden.")
        else:
            st.error("Bitte alle Felder ausfüllen.")

    st.header("Übersicht der Reservierungen")
    reservations = []
    
    for device in Device.find_all():
        for res in device.reservations:
            reservations.append({
                "Gerät": device.id,
                "Benutzer": device.managed_by_user_id,
                "Startdatum": res["start_date"],
                "Enddatum": res["end_date"]
            })

    if reservations:
        df = pd.DataFrame(reservations)
        st.table(df)
    else:
        st.info("Es gibt aktuell keine Reservierungen.")


    
def benutzerverwaltung():
    st.title("Nutzerverwaltung")
    
    tab1, tab2, tab3 = st.tabs(["Nutzerliste", "Nutzer hinzufügen", "Nutzer löschen"])

    with tab1:
        st.header("Nutzerliste")
        users = User.find_all()

        if users:
            for user in users:
                st.write(f"ID: {user.id}, Name: {user.name}, Erstellt: {user.creation_date}, Letzte Aktualisierung: {user.last_update}")
        else:
            st.info("Keine Nutzer gefunden.")

        if st.button("Liste aktualisieren"):
            st.rerun()

    with tab2:
        st.header("Nutzer hinzufügen")
        user_id = st.text_input("E-Mail-Adresse (ID)")
        user_name = st.text_input("Name des Nutzers")

        if st.button("Nutzer speichern"):
            if user_id and user_name:
                new_user = User(id=user_id, name=user_name)
                new_user.store_data()
                st.success(f"Nutzer {user_name} wurde erfolgreich hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte alle Felder ausfüllen.")

    with tab3:
        st.header("Nutzer löschen")
        users = User.find_all()

        if users:
            user_ids = [user.id for user in users]
            selected_user = st.selectbox("Nutzer auswählen", ["---"] + user_ids)

            if selected_user != "---":
                user_to_delete = next((user for user in users if user.id == selected_user), None)

                if st.button("Nutzer löschen"):
                    if user_to_delete:
                        user_to_delete.delete()
                        st.success(f"Nutzer {user_to_delete.name} wurde erfolgreich gelöscht!")
                        st.rerun()
                    else:
                        st.error("Nutzer konnte nicht gefunden werden.")
        else:
            st.info("Keine Nutzer verfügbar zum Löschen.")


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
                st.write(f"ID: {device.id}, Verantwortlicher: {device.managed_by_user_id}")
        else:
            st.info("Es sind keine Geräte in der Datenbank gespeichert.")

        if st.button("Geräteliste neu laden"):
            st.session_state["devices"] = Device.find_all()
            st.rerun()

    with tab2:
        st.header("Gerät hinzufügen")
        id = st.text_input("Gerätename", key="add_device_name")
        managed_by_user_id = st.text_input("Verantwortlicher Benutzer (ID)", key="add_managed_by_user_id")

        if st.button("Gerät speichern"):
            if id and managed_by_user_id:
                new_device = Device(id=id, managed_by_user_id=managed_by_user_id)
                new_device.store_data()
                st.success(f"Gerät '{id}' wurde erfolgreich hinzugefügt!")

                st.session_state["devices"] = Device.find_all()
            else:
                st.error("Bitte sowohl Gerätename als auch Benutzer-ID ausfüllen.")

    with tab3:
        st.header("Gerät bearbeiten oder löschen")
        st.write("Wähle ein Gerät aus der Liste aus.")

        device_names = [device.id for device in st.session_state["devices"]]
        selected_device = st.selectbox("Gerät auswählen", ["---"] + device_names)

        if selected_device != "---":
            selected_device_obj = next(device for device in st.session_state["devices"] if device.id == selected_device)

            st.subheader("Gerät bearbeiten")
            new_device_name = st.text_input("Neuer Gerätename", value=selected_device_obj.id, key="edit_device_name")
            new_managed_by_user_id = st.text_input("Neue Benutzer-ID", value=selected_device_obj.managed_by_user_id, key="edit_managed_by_user_id")

            if st.button("Änderungen speichern"):
                if new_device_name and new_managed_by_user_id:
                    selected_device_obj.id = new_device_name
                    selected_device_obj.managed_by_user_id = new_managed_by_user_id
                    selected_device_obj.store_data()
                    st.success(f"Gerät '{new_device_name}' wurde erfolgreich aktualisiert!")

                    st.session_state["devices"] = Device.find_all()
                    st.rerun()
                else:
                    st.error("Bitte sowohl neuen Gerätenamen als auch Benutzer-ID ausfüllen.")

            st.subheader("Gerät löschen")
            if st.button("Gerät löschen"):
                selected_device_obj.delete()
                st.success(f"Gerät '{selected_device}' wurde erfolgreich gelöscht!")
                st.session_state["devices"] = Device.find_all()
                st.rerun()


        
def geraetewartung():
    st.title("Wartungs-Management")
    tab1, tab2 = st.tabs(["Geräte anzeigen", "Wartungsdaten bearbeiten"])

    if "devices" not in st.session_state:
        st.session_state["devices"] = []

    if not st.session_state["devices"]:
        st.session_state["devices"] = Device.find_all()
    
    with tab1:
        st.header("Geräte mit vollständigen Wartungsdaten")
        complete_devices = []
        incomplete_devices = []
        
        for device in st.session_state["devices"]:
            if all(
                getattr(device, attr, None) is not None
                for attr in ["servicing_interval", "servicing_costs", "last_servicing", "next_servicing"]
            ):
                complete_devices.append(device)
            else:
                incomplete_devices.append(device)
        
        if complete_devices:
            for device in complete_devices:
                st.write(f"ID: {device.id}, Verantwortlicher: {device.managed_by_user_id}")
        else:
            st.info("Keine Geräte mit vollständigen Wartungsdaten gefunden.")
        
        st.header("Geräte mit fehlenden Wartungsdaten")
        if incomplete_devices:
            for device in incomplete_devices:
                st.write(f"ID: {device.id}, Verantwortlicher: {device.managed_by_user_id}")
        else:
            st.info("Alle Geräte haben vollständige Wartungsdaten.")

        if st.button("Geräteliste neu laden"):
            st.session_state["devices"] = Device.find_all()
            st.rerun()

    with tab2:
        st.header("Gerät bearbeiten")
        if st.session_state["devices"]:
            device_ids = [device.id for device in st.session_state["devices"]]
            selected_device_name = st.selectbox("Gerät auswählen", ["---"] + device_ids, key="device_select")

            if selected_device_name != "---":
                selected_device = next(device for device in st.session_state["devices"] if device.id == selected_device_name)

                st.write(f"### Bearbeitung von: {selected_device.id}")
                servicing_interval = st.number_input("Wartungsintervall (in Tagen)", value=getattr(selected_device, "servicing_interval", 0), key="serv_interval")
                servicing_costs = st.number_input("Wartungskosten", value=getattr(selected_device, "servicing_costs", 0.0), key="serv_costs")
                last_servicing = st.date_input("Letzte Wartung", value=getattr(selected_device, "last_servicing", datetime.now().date()), key="last_serv")

                if st.button("Speichern", key="save_device"):
                    selected_device.set_servicing_interval(servicing_interval)
                    selected_device.set_servicing_costs(servicing_costs)
                    selected_device.update_last_servicing()
                    selected_device.set_next_servicing(last_servicing + timedelta(days=servicing_interval) if servicing_interval else None)
                    selected_device.store_data()
                    st.success(f"Daten für Gerät '{selected_device.device_name}' wurden aktualisiert!")
                    st.session_state["devices"] = Device.find_all()
        else:
            st.info("Keine Geräte verfügbar.")
        
def generate_next_two_weeks():
    today = datetime.today()
    next_two_weeks = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(14)]
    return next_two_weeks


