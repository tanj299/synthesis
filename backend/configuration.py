#! env/bin/activate

# Authors: Jayson Tan 
# File: configuration.py
# Date Begun: 03/25/2020
# Last Updated: 04/10/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for configuring the initial Raspberry Pi 

import pymysql
import time 
from extensions import mysql
from flask import Flask, request, jsonify, Blueprint

config_api = Blueprint('config_api', __name__)

@config_api.route('/')
def index():
    return('Welcome to config!')

# GET request
# @GET: fetch user config from 'configuration' table 
# Requires a backslash at the end to query with an email
# Ex: janesmith@gmail.com OR janesmith%40gmail.com
@config_api.route('/<string:user_email>/', methods=['GET'])
def fetch_config(user_email): 
    try:
        connection = mysql.connect();
        cursor = connection.cursor(pymysql.cursors.DictCursor) 

        # fetch config match user_email
        cursor.execute("SELECT * FROM configuration WHERE user_email = %s", user_email)

        user = cursor.fetchone()
        response = jsonify(user)
        print(response)

        # if user_name not found 
        if user == None:
            print('Could not find username', user)
            response.status_code = 404
        else: 
            response.status_code = 200
        
        return response
    except:
        print('Could not fetch user', user)
    finally: 
        connection.close()
        cursor.close()

if __name__ == ("__main__"):
    app.run(debug=True)
