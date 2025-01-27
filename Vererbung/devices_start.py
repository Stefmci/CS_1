import os
from datetime import datetime
from typing import Self
from tinydb import TinyDB, Query
from database import DatabaseConnector
from serializable_start import Serializable


class Device(Serializable):
    # Class variable that is shared between all instances of the class
    db_connector =  DatabaseConnector().get_table("devices")

    def __init__(self, id: str, managed_by_user_id: str, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None):
        super().__init__(id, creation_date, last_update)
        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.end_of_life = end_of_life if end_of_life else datetime.today().date()
        
    # String representation of the class
    def __str__(self):
        return f'Device (Object) {self.id} ({self.managed_by_user_id})'
    
    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id

    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['id'], data['managed_by_user_id'], data['creation_date'], data['last_update'])


if __name__ == "__main__":
    # Create a device
    device1 = Device("Device1", "one@mci.edu")
    device2 = Device("Device2", "two@mci.edu") 
    device3 = Device("Device3", "two@mci.edu") 
    device4 = Device("Device4", "two@mci.edu") 
    device1.store_data()
    device2.store_data()
    device3.store_data()
    device4.store_data()
    device5 = Device("Device3", "four@mci.edu") 
    device5.store_data()

    #loaded_device = Device.find_by_attribute("device_name", "Device2")
    loaded_device = Device.find_by_attribute("id", "Device2")
    if loaded_device:
        print(f"Loaded Device: {loaded_device}")
    else:
        print("Device not found.")

    devices = Device.find_all()
    print("All devices:")
    for device in devices:
        print(device)

    