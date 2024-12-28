import streamlit as st

# Eine Überschrift der ersten Ebene
st.write("# Geräteverwaltung")

# Eine Überschrift der zweiten Ebene
st.write("### Bitte wählen Sie eine Aktion um sie durchzuführen!")

selected_action = st.button(label="Geräte-Verwaltung"), st.button(label="Nutzer-Verwaltung"), st.button(label="Reservierungssystem"), st.button(label="Wartungs-Management")