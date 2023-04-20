import random
from hashlib import *


def salt_hash(password, salt, count):
    hashed = salt + password
    salt = b"SHA256:" + str(count).encode() + salt
    for i in range(count):
        hashed = sha256(hashed).hexdigest().encode()
    hashed = salt.decode() + hashed.decode()
    return hashed


def password_to_hash(password: str):
    password = password.encode()
    count = random.randint(500, 900)
    salt = ""
    for i in range(20):
        salt += chr(random.randint(33, 126))
    salt = sha256(salt.encode()).hexdigest()[:26].encode()
    return salt_hash(password, salt, count)


def verify_password_hash(password, hashed):
    count = int(hashed[7:10])
    salt = hashed[10:36].encode()
    return salt_hash(password.encode(), salt, count) == hashed


if __name__ == "__main__":
    password = "test"
    hashed = password_to_hash(password)
    print(password)
    print(hashed)
    print(verify_password_hash(password, hashed))
