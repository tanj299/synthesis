#! env/bin/activate

# Authors: Jayson Tan
# File: login.py
# Date Begun: 04/16/2020
# Last Updated: 04/16/2020

# DUMMY FILE
# Use for testing functions because sometimes, 
#   you can't be too sure of the documentation you read

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from userClass import User

# Testing password hashing and check password hash using werkzeug.security
hash = generate_password_hash('foobar')

if check_password_hash(hash, 'boob'):
    print('Password matches', hash)

else: 
    print('Password does not match')

dummy = User()
dummy.id = 5
dummy.username = "Bob"
dummy.password = "adfsagadlfjaj"
hashD = generate_password_hash(dummy.password)


# encode() converts string into bytes to be acceptable by hash function
# hexdigest() returns encoded data into hexadecimal format
# does match with database aes_encrypt 256
password = "johnsmith"
result = hashlib.sha256(password.encode())
print("sha256: ", result.hexdigest())

print(dummy.id, dummy.username, dummy.password, hashD)