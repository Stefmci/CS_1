from tinydb import Query, TinyDB
from database import Database
from serializer import serializer
import os
import streamlit as st
import database as datab

class User:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        self.name = name
        self.id = id

    def store_data(self):
        try:
            User.db_connector.upsert({"id": self.id, "name": self.name}, Query().id == self.id)
        except Exception as e:
            raise Exception(f"Fehler beim Speichern des Benutzers: {e}")

    def delete(self):
        try:
            User.db_connector.remove(Query().id == self.id)
        except Exception as e:
            raise Exception(f"Fehler beim Löschen des Benutzers: {e}")

    def __str__(self):
        return f"User {self.id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def find_all(cls) -> list:
        users = []
        for user_data in cls.db_connector.all():
            users.append(cls(user_data['id'], user_data['name']))
        return users

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        UserQuery = Query()
        result = cls.db_connector.search(UserQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            user_results = [cls(d['id'], d['name']) for d in data]
            return user_results if num_to_return > 1 else user_results[0]
        else:
            return None


def list_users():
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


def add_user():
    st.header("Nutzer hinzufügen")
    user_name = st.text_input("Benutzername")
    user_id = st.text_input("E-Mail-Adresse")
    if st.button("Benutzer speichern"):
        if user_name:
            try:
                user_id = str(datab.generate_user_id())  # ID als String sicherstellen
                user = User(user_id, user_name)
                user.store_data()
                st.success(f"Benutzer {user_name} (ID: {user_id}) wurde hinzugefügt!")
            except Exception as e:
                st.error(f"Fehler beim Speichern des Benutzers: {e}")
        else:
            st.error("Bitte einen Namen eingeben.")


def delete_user():
    st.header("Benutzer löschen")
    del_user_id = st.text_input("ID des zu löschenden Benutzers")
    if st.button("Benutzer löschen"):
        if del_user_id:
            try:
                user = User.find_by_attribute("id", del_user_id)
                if user:
                    user.delete()
                    st.success(f"Benutzer mit ID {del_user_id} wurde gelöscht!")
                else:
                    st.warning(f"Benutzer mit ID {del_user_id} wurde nicht gefunden.")
            except Exception as e:
                st.error(f"Fehler beim Löschen des Benutzers: {e}")
        else:
            st.error("Bitte eine Benutzer-ID eingeben.")



