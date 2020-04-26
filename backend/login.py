#! env/bin/activate

# Authors: Jayson Tan
# File: login.py
# Date Begun: 04/16/2020
# Last Updated: 04/16/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for logging users 

import pymysql
import hashlib
import time
from userClass import User 
from extensions import mysql
from flask import jsonify, Flask, flash, request, Blueprint, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

# Werkzeug library used to verify user password matches with the DB password
# Flask-Login extension manages login state and user sessions

# Blueprint object for login
login_api = Blueprint('login_api', __name__)

# New user object 
new_user = User() 

@login_api.route('/')
def index():
    return('Welcome to login!')

@login_api.route('/login_page', methods=['GET', 'POST'])
def login():
    msg = 'Oops, cannot login' 

    # Check if 'username' and 'password' POST requehttps://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encrypthttps://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_aes-encryptsts exist in the client-side form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        new_user.id = request.form['id']
        new_user.username = request.form['username']
        new_user.password = request.form['password']

        # encode() converts string to bytes to allow password to be hashable
        # hexdigest() returns encode data into hexadecimal format
        hashed_password = hashlib.sha256(new_user.password.encode())
        hashed_hex = hashed_password.hexdigest()

        # DL
        print("Username, password, and hashed password: ", new_user.username, new_user.password, hashed_hex)

        # Check if account exists in database 
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        # DL: id works 
        # cursor.execute("SELECT * FROM users WHERE id = %s", new_user.id)

        sqlQuery = "SELECT * FROM users WHERE username = %s AND password = %s"
        recordTuple = (new_user.username, hashed_hex)
        cursor.execute(sqlQuery, recordTuple) 

        # POSTMAN requirements:
        '''
        HEADERS: Key: Content-Type, Value: application/json
        BODY: form-data
        '''

        # Sample body:
        '''
        KEY: username | VALUE: johnsmith
        KEY: password | VALUE: johnsmith
        KEY: id       | VALUE: 1
        '''

        # Fetch one record 
        account = cursor.fetchone()
        response = jsonify(account)

        # # DL
        # print("Account: ", account)

        # if account: 
        #     return("Account found!")
        # else:
        #     return("Account not found")
            
        # If account exists in our `users` table in our database 
        if account: 
            # Create session for the user so user can access other routes
            session['loggedin'] = True 
            session['id'] = account['id']
            session['username'] = account['username']

            # If successful, set new_user.is_logged_in to True

            return 'Logged in successfully!'
        else: 
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'

    # return redirect(url_for('/'))








    
