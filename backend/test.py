#! env/bin/activate

# Authors: Jayson Tan
# File: login.py
# Date Begun: 04/16/2020
# Last Updated: 04/16/2020

# DUMMY FILE
# Use for testing functions because sometimes, 
#   you can't be too sure of the documentation you read

from werkzeug.security import generate_password_hash, check_password_hash


# Testing password hashing and check password hash using werkzeug.security
hash = generate_password_hash('foobar')

if check_password_hash(hash, 'boob'):
    print('Password matches', hash)

else: 
    print('Password does not match')
