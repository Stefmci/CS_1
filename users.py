from tinydb import Query, TinyDB
from database import Database
from serializer import serializer
import os
import streamlit as st

class User:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')
    
    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name
        self.id = id
        

    def store_data(self)-> None:
        """Store the user data in the database"""
        print("Storing data...")
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.id == self.id)
        if result:
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    def delete(self) -> None:
        """Delete the user from the database"""
        print("Deleting data...")
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.id == self.id)
        if result:
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")
    
    def __str__(self):
        return f"User {self.id} - {self.name}"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def find_all(cls) -> list:
        """Find all users in the database"""
        users = []
        for user_data in User.db_connector.all():
            users.append(User(user_data['id'], user_data['name']))
        return users

    @classmethod
    def find_by_attribute(cls, by_attribute : str, attribute_value : str, num_to_return=1) -> 'User':
        """From the matches in the database, select the user with the given attribute value"""
        UserQuery = Query()
        result = cls.db_connector.search(UserQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            user_results = [cls(d['id'], d['name']) for d in data]
            return user_results if num_to_return > 1 else user_results[0]
        else:
            return None
