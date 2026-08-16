import crypto
import storage
from cryptography.fernet import InvalidToken

def request_master_password(master_password):
    all_data = storage.list_all()
    first_entry = all_data[0]
    first_entry_id = first_entry[1]
    attempt = storage.lookup_id(first_entry_id) # encrypted_data, salt
    #key = crypto.derive_key(master_password, attempt[1]) dead code! more dead code! KILL
    try:
         #decrypted = crypto.decrypt_entry(attempt[0], key) dead code lol
         return True
    except InvalidToken:
         return False
         

def retrieve_entry(master_password, entry_id):
     specific_data = storage.lookup_id(entry_id)
     key = crypto.derive_key(master_password, specific_data[1])
     try:
         decrypted = crypto.decrypt_entry(specific_data[0], key)
         return decrypted
     except InvalidToken:
         return False

def new_entry(master_password, service_name, user_email, password):
     login_information = {
          "user_or_email": user_email,
          "password": password}
     salt = crypto.generate_salt()
     key = crypto.derive_key(master_password, salt)
     encrypted = crypto.encrypt_entry(login_information, key)
     storage.add_entry(service_name, encrypted, salt)