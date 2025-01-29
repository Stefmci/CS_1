import os
from tinydb import TinyDB, Query
from serializer import serializer
from datetime import datetime, timedelta
import reservation_service as rs


class Device():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    def __init__(self, id: str,
                 managed_by_user_id: str,
                 is_active: bool = True,
                 end_of_life: datetime = None,
                 servicing_interval: int = None,
                 servicing_costs: float = None,
                 last_servicing: datetime = None,
                 next_servicing: datetime = None,
                 reservations: list = None,
                 creation_date: datetime = None,
                 last_updated: datetime = None):

        self.device_name = id
        self.managed_by_user_id = managed_by_user_id
        self.is_active = is_active
        self.end_of_life = end_of_life if end_of_life else datetime.now().date() + timedelta(days=365)
        self.servicing_interval = servicing_interval
        self.servicing_costs = servicing_costs
        self.last_servicing = last_servicing
        self.next_servicing = next_servicing
        self.reservations = reservations or []
        self.creation_date = creation_date if creation_date else datetime.now().date()
        self.last_updated = last_updated if last_updated else datetime.now().date()

        if not servicing_interval:
            self.servicing_interval = None
        if not servicing_costs:
            self.servicing_costs = None
        if not last_servicing:
            self.last_servicing = None
        if not next_servicing:
            self.next_servicing = None
        
    def __str__(self):
        return f'Device (Object) {self.device_name} ({self.managed_by_user_id})'

    def store_data(self):
        print("Storing data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")
            
    def update_last_servicing(self):
        self.last_servicing = datetime.now().date()
        
    def set_end_of_life(self, end_of_life: datetime):
        self.end_of_life = end_of_life

    def set_servicing_interval(self, servicing_interval: int):
        self.servicing_interval = servicing_interval
        self.set_next_servicing()
        self.store_data()

    def set_servicing_costs(self, servicing_costs: float):
        self.servicing_costs = servicing_costs
        
    def set_next_servicing(self, next_servicing: datetime):
        self.next_servicing = self.creation_date + timedelta(days = self.servicing_interval)  
    
    def calculate_quarterly_servicing_costs(self):
        if not self.servicing_interval or not self.servicing_costs:
            return 0
        
    def create_reservation(self, user_id: str, start_date: datetime, end_date: datetime) -> bool:
        if not hasattr(self, 'reservations') or self.reservations is None:
            self.reservations = []

        for existing in self.reservations:
            start_existing = datetime.strptime(existing['start_date'], '%Y-%m-%d').date()
            end_existing = datetime.strptime(existing['end_date'], '%Y-%m-%d').date()
            
            if (start_existing <= end_date and start_date <= end_existing):
                return False
        
        self.reservations.append({
            "user_id": user_id,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d')
        })

        self.store_data()
        return True

    
    def delete(self):
        print("Deleting data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")

    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            device_results = [cls(**d) for d in data]
            return device_results if num_to_return > 1 else device_results[0]
        else:
            return None

    @classmethod
    def find_all(cls) -> list:
        devices = []
        for device_data in Device.db_connector.all():
            devices.append(Device(
                id=device_data.get('id'),
                managed_by_user_id=device_data.get('managed_by_user_id'),
                is_active=device_data.get('is_active', True),
                end_of_life=device_data.get('end_of_life'),
                servicing_interval=device_data.get('servicing_interval'),
                servicing_costs=device_data.get('servicing_costs'),
                last_servicing=device_data.get('last_servicing'),
                next_servicing=device_data.get('next_servicing'),
                reservations=device_data.get('reservations', []),
                creation_date=device_data.get('creation_date'),
                last_updated=device_data.get('last_updated')
            ))
        return devices



    