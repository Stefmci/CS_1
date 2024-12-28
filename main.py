import streamlit as st
from user_management import user_management_page

def main():
    st.title("Systemverwaltung")

    # Navigation buttons
    if st.button("Geräte-Verwaltung"):
        st.write("Navigating to Geräte-Verwaltung...")
    elif st.button("Nutzer-Verwaltung"):
        st.session_state["page"] = "nutzer_verwaltung"
    elif st.button("Reservierungssystem"):
        st.write("Navigating to Reservierungssystem...")
    elif st.button("Wartungs-Management"):
        st.write("Navigating to Wartungs-Management...")

    # Page Navigation
    if st.session_state.get("page") == "nutzer_verwaltung":
        user_management_page()

if __name__ == "__main__":
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state["page"] = "main"
    main()