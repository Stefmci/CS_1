import streamlit as st
from queries import find_devices
from devices import Device
from datetime import datetime, timedelta


# Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
devices_in_db = find_devices()

if devices_in_db:
    current_device_name = st.selectbox(
        'Gerät auswählen',
        options=devices_in_db, key="sbDevice")

    if current_device_name in devices_in_db:
        loaded_device = Device.find_by_attribute("device_name", current_device_name)
        if loaded_device:
            st.write(f"Loaded Device: {loaded_device}")
        else:
            st.error("Device not found in the database.")

        with st.form("Device"):
            st.write(loaded_device.device_name)

            text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
            loaded_device.set_managed_by_user_id(text_input_val)

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                loaded_device.store_data()
                st.write("Data stored.")
                st.rerun()
    else:
        st.error("Selected device is not in the database.")
else:
    st.write("No devices found.")
    st.stop()
    
def generate_next_two_weeks():
    today = datetime.today()
    next_two_weeks = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(14)]
    return next_two_weeks

dates = generate_next_two_weeks()

st.write("Session State:")
st.session_state


def Reservierung():
    st.title("Reservierung")
    st.write("Hie können Sie ein Gerät reservieren")
    st.selectbox("Gerät auswählen", ["Laserschneider", "3D-Drucker", "CNC-Fräse", "Schweißgerät", "Lötkolben", "Oszilloskop", "Multimeter", "Netzteil", "Funktionsgenerator"])
    st.selectbox("Datum auswählen", [ui.dates()] )

def benutzerverwaltung():
    st.title("Benutzerverwaltung")
    st.write("Hier kannst du Benutzer hinzufügen oder verwalten.")
    st.header("Benutzerliste:")
    
    st.header("Benutzer hinzufügen")
    user_id = st.text_input("Benutzer-ID")
    user_name = st.text_input("Benutzername")
    if st.button("Benutzer speichern"):
        st.success(f"Benutzer {user_name} mit ID {user_id} wurde hinzugefügt!")

def geraeteverwaltung():
    st.title("Geräteverwaltung")
    st.write("Hier kannst du Geräte hinzufügen oder verwalten.")
    
    st.header("Gerät hinzufügen")
    device_id = st.text_input("Geräte-ID")
    device_name = st.text_input("Gerätename")
    if st.button("Gerät speichern"):
        st.success(f"Gerät {device_name} mit ID {device_id} wurde hinzugefügt!")
        
def geraetewartung():
    st.title("Wartungs-Management")
    st.write("Hier kannst du Geräte hinzufügen oder verwalten.")
    st.header("Geräte anpassen")
    
    st.header("Gerät hinzufügen")
    device_id = st.text_input("Geräte-ID")
    device_name = st.text_input("Gerätename")
    if st.button("Gerät speichern"):
        st.success(f"Gerät {device_name} mit ID {device_id} wurde hinzugefügt!")