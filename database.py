from tinydb import TinyDB, Query

class Database:
    DB_FILE = "database.json"

    def __init__(self):
        self.db = TinyDB(self.DB_FILE)

    def get_table(self, table_name: str):
        return self.db.table(table_name)

    def close(self):
        self.db.close()
