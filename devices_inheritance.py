from typing import Self
from datetime import datetime
from serializable import Serializable
from database import DatabaseConnector

class Device(Serializable):

    db_connector =  DatabaseConnector().get_table("devices")

    def __init__(self, id: str, managed_by_user_id: str, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None):
        super().__init__(id, creation_date, last_update)
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.end_of_life = end_of_life if end_of_life else datetime.today().date()
   
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['id'], data['managed_by_user_id'], data['end_of_life'], data['creation_date'], data['last_update'])

    def __str__(self) -> str:
        return F"Device: {self.id} ({self.managed_by_user_id}) - Active: {self.is_active} - Created: {self.creation_date} - Last Update: {self.last_update}"

    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id
    
    