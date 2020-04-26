#! env/bin/activate

# Authors: Jayson Tan
# File: logs.py
# Date Begun: 04/19/2020
# Last Updated: 04/25/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for logging information to the database from Raspberry Pi


import time
import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint, redirect

logs_api = Blueprint('logs_api', __name__)

@logs_api.route('/')
def index():
    return('Welcome to logs!')
    # return redirect('http://www.google.com', code=302)

# GET request
# @GET: Fetch all logs
@logs_api.route('/all', methods=['GET'])
def fetch_all_logs(): 
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Fetch all logs 
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except:
        print("Could not fetch all logs from database")
    finally: 
        connection.close()
        cursor.close()


# GET request
# @GET: Fetch latest log from user 
@logs_api.route('/<int:id>', methods=['GET'])
def fetch_log(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Query for the latest log entry from a user id based on timestamp
        cursor.execute(
            "SELECT t1.* FROM logs AS t1 WHERE t1.timestamp = (SELECT MAX(t2.timestamp) FROM logs AS t2 WHERE t2.plant_id = t1.plant_id) HAVING plant_id = %s", id)
        single_request = cursor.fetchone()
        response = jsonify(single_request)

        return response
    except:
        return('Could not FETCH logs id')
    finally:
        connection.close()
        cursor.close()

# POST request
# POST a log from user
@logs_api.route('/insert', methods=['POST'])
def post_latest():     

    # grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    plant_id = request.json['plant_id']
    timestamp = request.json['timestamp']
    light = request.json['light']
    temp = request.json['temp']
    humidity = request.json['humidity']
    soil_temp = request.json['soil_temp']
    soil_moisture = request.json['soil_moisture']
    water_level = request.json['water_level']

    # POSTMAN requirements: 
    '''
    HEADERS: Key: Content-Type, Value: application/json
    BODY: raw
    '''
    
    # Note: "timestamp" field should be an empty string since backend Python will take care of datetime
    # Sample body:
    '''
    {
        "plant_id": 2, 
        "timestamp": "", 
        "light": 100,
        "temp": 90,
        "humidity": 80,
        "soil_temp": 70,
        "soil_moisture": 60,
        "water_level": 50
    }
    '''

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO logs(plant_id, timestamp, light, temp, humidity, soil_temp, soil_moisture, water_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    recordTuple = (plant_id, now, light, temp, humidity,
                   soil_temp, soil_moisture, water_level)

    data = {"plant_id": plant_id,
            "timestamp": now,
            "light": light,
            "temp": temp,
            "humidity": humidity,
            "soil_temp": soil_temp,
            "soil_moisture": soil_moisture,
            "water_level": water_level
            }

    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Insert log into `logs` table
        # Pass sqlQuery and recordTuple as arguments
        cursor.execute(sqlQuery, recordTuple)

        # Commit record to database so new record persists
        connection.commit()
        return jsonify(data)
    except:
        print('Could not POST a new request')
        return('Request failed: ensure that the plant exists and the plant_id matches with the `plants` table')
    finally:
        connection.close()
        cursor.close()

# HTTP response with 404 error
@logs_api.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


