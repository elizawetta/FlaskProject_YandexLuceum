import hashlib
import os


def make_hash_password(password: str):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt, key


def check_password(salt, password, new_password):
    key = hashlib.pbkdf2_hmac('sha256', new_password.encode('utf-8'), salt, 100000)
    return key == password
