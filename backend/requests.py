#! env/bin/activate

# Authors: Jayson Tan
# File: requests.py
# Date Begun: 04/19/2020
# Last Updated: 04/25/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for making requests to the Raspberry Pi

import time
import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

requests_api = Blueprint('requests_api', __name__)

request
@requests_api.route('/')
def index():
    return('Welcome to requests!')

# GET request
# @GET: Fetch latest request submitted from a user
@requests_api.route('/<int:id>', methods=['GET'])
def get_latest(id):
    try: 
        connection = mysql.connect() 
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Query reads as follows:
        # Select all columns from requests where we alias the table as t1, such that (the WHERE clause) the t1's timestamp is equal to
        #   the max timestamp from requests aliased by table, t2, having plant_id matching the queried id 
        cursor.execute("SELECT t1.* FROM requests AS t1 WHERE t1.timestamp = (SELECT MAX(t2.timestamp) FROM requests AS t2 WHERE t2.plant_id = t1.plant_id) HAVING plant_id = %s", id)
        # cursor.execute("SELECT * FROM requests WHERE plant_id = %s", id)
        single_request = cursor.fetchone()
        response = jsonify(single_request)
        response.status_code = 200
        return response 
    except:
        print('Could not FETCH request id')
        return('Could not FETCH request id')
    finally: 
        connection.close()
        cursor.close()

# POST request
# @POST: Create a request to affect the sensors 
@requests_api.route('/insert', methods=['POST'])
def post_latest():

    # grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    plant_id = request.json['plant_id']
    timestamp = request.json['timestamp']
    arduino = request.json['arduino']
    pin = request.json['pin']
    make_request = request.json['make_request']
    on_off = request.json['on_off']
    error = request.json['error']

    # POSTMAN requirements:
    '''
    HEADERS: Key: Content-Type, Value: application/json
    BODY: raw
    '''

    # Sample body:
    # Note: "timestamp" field should be an empty string since backend Python will take care of datetime
    '''
    {
        "plant_id": 5, 
        "timestamp": "",
        "arduino": "16",
        "pin": "8", 
        "make_request":1,
        "on_off":1,
        "error":1
    }
    '''

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO requests(plant_id, arduino, pin, make_request, on_off, error, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    recordTuple = (plant_id, arduino, pin, make_request, on_off, error, now)
    # DL: recordTuple = ('agentsmith@aol.com', 'perry the platypus', 'snake-tree', 'http://sample.com/', 3, now)
    
    data = {"plant_id": plant_id,
            "timestamp": now,
            "arduino": arduino,
            "pin": pin,
            "make_request": make_request,
            "on_off": on_off,
            "error": error
            }

    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Insert request into `requests` table
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
@requests_api.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Execute `flask run` instead")
