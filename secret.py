import math
import random
import bcrypt
from sympy import randprime

def are_coprime(a, b):
    return math.gcd(a, b) == 1

def secret():
    p = randprime(2 ** 1023, 2 ** 1024 - 1)
    q = randprime(2 ** 1023, 2 ** 1024 - 1)
    while p % q == 0 or q % p == 0:
        p = randprime(2 ** 1023, 2 ** 1024 - 1)
        q = randprime(2 ** 1023, 2 ** 1024 - 1)
    n = p * q
    fin = (p - 1) * (q - 1)
    e = 65537
    while not are_coprime(e, fin):
        e += 1
    k = 1
    while (fin * k + 1) % e != 0:
        k += 1
    d = (fin * k + 1) // e
    return n, e, d

def resecret(num_hex):
    print("recive")
    with open("key", 'r') as f:
        key = int(f.read())
    with open("modn", 'r') as f:
        n = int(f.read())
    num_b = bin((int(num_hex, 16)**key)%n)[2:]
    num_str = ""
    for i in range(len(0,num_b, 8)):
        num_str = num_str + chr(int(num_b[i:i+8], 2))
    print("finish")
    return num_str

def mk_hash(password):
    password_b = password.encode("UTF-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_b, salt)
    return hashed

def check_password(password, hashed):
    password_b = password.encode("UTF-8")
    return bcrypt.checkpw(password_b, hashed)

def set_key():
    modn, pub_key, key = secret()
    with open("key", 'w') as f:
        f.write(str(key))
    with open("pub_key", 'w') as f:
        f.write(str(pub_key))
    with open("modn", 'w') as f:
        f.write(str(modn))

if __name__ == "__main__":
    pass