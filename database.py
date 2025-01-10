from tinydb import TinyDB, Query

class Database:
    DB_FILE = "database.json"

    def __init__(self):
        self.db = TinyDB(self.DB_FILE)

    def get_table(self, table_name: str):
        return self.db.table(table_name)

    def close(self):
        self.db.close()


def generate_user_id():
    db = TinyDB(Database.DB_FILE).table("user_ids")
    if not db.contains(Query().type == "user_ids"):
        db.insert({"type": "user_ids", "current_id": 0})
    user_id_entry = db.get(Query().type == "user_ids")
    new_id = user_id_entry["current_id"] + 1
    db.update({"current_id": new_id}, Query().type == "user_ids")
    return new_id
