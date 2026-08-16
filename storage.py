import sqlite3
import os # instead of hardcoding the path to the database, maybe i should use this to get the path of the db file regardless of where its located?

app_data_dir = os.getenv("APPDATA")
app_folder = os.path.join(app_data_dir, "Moha's Password Manager")
os.makedirs(app_folder, exist_ok=True)
DB_PATH = os.path.join(app_folder, "teehee.db")


def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ENTRY (service_name TEXT, encrypted_data BLOB, salt BLOB, ID INTEGER PRIMARY KEY);")
    conn.close()

def add_entry(service_name, encrypted_data, salt):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ENTRY (service_name, encrypted_data, salt) VALUES (?, ?, ?)", (service_name, encrypted_data, salt))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def search_entries(service_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        pattern = f"%{service_name}%"
        cursor.execute("SELECT SERVICE_NAME, ID FROM ENTRY WHERE SERVICE_NAME LIKE ?", (pattern,))
        fetch = cursor.fetchall()
        cursor.close()
    conn.close()
    return fetch

def list_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SERVICE_NAME, ID FROM ENTRY")
    fetching_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return fetching_data

def delete_entry(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ENTRY WHERE ID = ?", (entry_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Entry with ID {entry_id} deleted successfully")


def lookup_id(entry_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_data, salt FROM ENTRY WHERE ID = ?", (entry_id, ))
        fetch = cursor.fetchone()        
        cursor.close()
    conn.close()
    return fetch # i know lookup_id is different from the rest, i was just testing out with for the first time lol