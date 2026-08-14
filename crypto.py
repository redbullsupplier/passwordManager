import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
import base64
from cryptography.fernet import Fernet
import json
import string
import secrets


def derive_key(master_password, salt):
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=1,
        lanes=4,
        memory_cost=2**21
    )
    raw_key = kdf.derive(master_password.encode())
    fernet_key = base64.urlsafe_b64encode(raw_key)
    return fernet_key

def generate_salt():
    salt = os.urandom(16)
    return salt

def encrypt_entry(user_dict, key):
    into_string = json.dumps(user_dict)
    raw_string = into_string.encode() # fernet needs the string as bytes
    encrypted = Fernet(key).encrypt(raw_string)
    return encrypted

def decrypt_entry(encrypted_string, key):
    decrypted = Fernet(key).decrypt(encrypted_string)
    decrypted_string = decrypted.decode()
    into_dict = json.loads(decrypted_string)
    return into_dict

def generate_password(length = 8):
    pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    lower = secrets.choice(string.ascii_lowercase)
    upper = secrets.choice(string.ascii_uppercase)
    digits = secrets.choice(string.digits)
    punctuation = secrets.choice(string.punctuation)
    remaining = length - 4
    rest = [secrets.choice(pool) for i in range(remaining)]
    passwordlist = [upper, lower, digits, punctuation] + rest
    secrets.SystemRandom().shuffle(passwordlist)
    return "".join(passwordlist)