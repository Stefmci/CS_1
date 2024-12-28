import streamlit as st

def startseite():
    st.title("Willkommen ")
    st.divider()
    st.header("bei der Geräteverwaltung der Hochschule")
    st.write("Am linken Rand befindet sich die Navigation, wo Sie zwischen den verschiedenen Seiten wechseln können.")
    st.title("News")
    st.write("Nächste Woche ist die CNC-Fräse nicht verfügbar.")
    st.write("Bei Fragen oder Problemen wenden Sie sich bitte an den Administrator.")



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