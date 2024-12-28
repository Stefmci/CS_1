import streamlit as st
from users import User

def user_management_page():
    st.title("Nutzer-Verwaltung")

    if st.button("Nutzer anlegen"):
        st.session_state["page"] = "nutzer_anlegen"

    if st.session_state.get("page") == "nutzer_anlegen":
        create_user_page()

def create_user_page():
    st.title("Neuen Nutzer anlegen")

    # Form for creating a new user
    with st.form("create_user_form"):
        username = st.text_input("Benutzername:")
        email = st.text_input("E-Mail-Adresse:")
        submitted = st.form_submit_button("Nutzer speichern")

        if submitted:
            # Save the user in the database
            user = User(id=email, name=username)  # Use email as ID
            user.store_data()
            st.success(f"Nutzer {username} mit der E-Mail {email} wurde erfolgreich angelegt!")
