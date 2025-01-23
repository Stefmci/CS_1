import os
from tinydb import TinyDB, Query
from database import DatabaseConnector
from typing import Self
from datetime import datetime

class User:
    db_connector =  DatabaseConnector().get_table("users")

    # Constructor
    def __init__(self, name, id) -> None:
        self.name = name
        super().__init__(id, creation_date=datetime.now(), last_update=datetime.now())
        
    # String representation of the class
    def __str__(self):
        return f'User (Object) {self.id}'

    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['name'], data['id'])

if __name__ == "__main__":
    # Create a device
    user1 = User("User One", "one@mci.edu")
    user2 = User("User Two", "two@mci.edu") 
    user3 = User("User Three", "three@mci.edu") 
    user1.store_data()
    user2.store_data()
    user3.store_data()
    user4 = User("User Four", "four@mci.edu") 
    user4.store_data()

    loaded_user = User.find_by_attribute("id", "three@mci.edu")
    if loaded_user:
        print(f"Loaded: {loaded_user}")
    else:
        print("User not found.")