import sqlite3


def create_table():
    with sqlite3.connect("teehee.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ENTRY (service_name TEXT, encrypted_data BLOB, salt BLOB, ID INTEGER PRIMARY KEY);")
    conn.close()

def add_entry(service_name, encrypted_data, salt):
    conn = sqlite3.connect("teehee.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ENTRY (service_name, encrypted_data, salt) VALUES (?, ?, ?)", (service_name, encrypted_data, salt))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def lookup_entry(service_name):
    conn = sqlite3.connect("teehee.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SERVICE_NAME, ENCRYPTED_DATA, SALT, ID FROM ENTRY WHERE SERVICE_NAME = (?)", (service_name,))
    fetching_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return fetching_data

def list_all():
    conn = sqlite3.connect("teehee.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SERVICE_NAME, ID FROM ENTRY")
    fetching_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return fetching_data

def delete_entry(entry_id):
    conn = sqlite3.connect("teehee.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ENTRY WHERE ID = ?", (entry_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Entry with ID {entry_id} deleted successfully")


def lookup_id(entry_id):
    with sqlite3.connect("teehee.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_data, salt FROM ENTRY WHERE ID = ?", (entry_id, ))
        fetch = cursor.fetchone()        
        cursor.close()
    conn.close()
    return fetch # i know lookup_id is different from the rest, i was just testing out with for the first time lol