import streamlit as st

# Funktion für die Startseite
def startseite():
    st.title("Startseite")
    st.write("Willkommen auf der Startseite!")

# Funktion für die Benutzerverwaltung
def benutzerverwaltung():
    st.title("Benutzerverwaltung")
    st.write("Hier kannst du Benutzer hinzufügen oder verwalten.")
    
    # Beispiel für Benutzer hinzufügen
    st.header("Benutzer hinzufügen")
    user_id = st.text_input("Benutzer-ID")
    user_name = st.text_input("Benutzername")
    if st.button("Benutzer speichern"):
        st.success(f"Benutzer {user_name} mit ID {user_id} wurde hinzugefügt!")

# Funktion für die Geräteverwaltung
def geraeteverwaltung():
    st.title("Geräteverwaltung")
    st.write("Hier kannst du Geräte hinzufügen oder verwalten.")
    
    # Beispiel für Gerät hinzufügen
    st.header("Gerät hinzufügen")
    device_id = st.text_input("Geräte-ID")
    device_name = st.text_input("Gerätename")
    if st.button("Gerät speichern"):
        st.success(f"Gerät {device_name} mit ID {device_id} wurde hinzugefügt!")

# Sidebar-Navigation
st.sidebar.title("Navigation")
auswahl = st.sidebar.radio("Seite auswählen", ["Startseite", "Benutzerverwaltung", "Geräteverwaltung"])

# Logik zur Auswahl der Seite
if auswahl == "Startseite":
    startseite()
elif auswahl == "Benutzerverwaltung":
    benutzerverwaltung()
elif auswahl == "Geräteverwaltung":
    geraeteverwaltung()
