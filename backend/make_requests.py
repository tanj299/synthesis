#! env/bin/activate

# Authors: Jayson Tan
# File: make_requests.py
# Date Begun: 04/19/2020
# Last Updated: 04/25/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for making requests to the Raspberry Pi


import time
import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

requests_api = Blueprint('requests_api', __name__)

@requests_api.route('/')
def index():
    return('Welcome to requests!')


# MODIFY POST request: Client will send a request in plain English to category and use conditionals to deal with it
# water, light, take_picture

# POST request
# @POST: Create a request to affect the sensors
@requests_api.route('/insert/<string:category>', methods=['POST'])
def post_latest(category):

    # Grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    plant_id = request.json['plant_id']
    timestamp = request.json['timestamp']
    arduino = request.json['arduino']
    pin = request.json['pin']
    make_request = request.json['make_request']

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
    }
    '''

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO requests(plant_id, arduino, pin, make_request, timestamp) VALUES (%s, %s, %s, %s, %s)"
    recordTuple = (plant_id, arduino, pin, make_request, now)
    # DL: recordTuple = ('agentsmith@aol.com', 'perry the platypus', 'snake-tree', 'http://sample.com/', 3, now)

    data = {"plant_id": plant_id,
            "timestamp": now,
            "arduino": arduino,
            "pin": pin,
            "make_request": make_request,
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

# GET request 
# @GET: Fetch all records from a user after a sent timestamp
@requests_api.route('/all/<int:id>/<string:time>', methods=['GET'])
def get_latest_time(id, time):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM requests WHERE plant_id = %s AND timestamp >= %s", (id, time))
        rows = cursor.fetchall()
        response = jsonify(rows)
        return response
    except:
        print('Could not FETCH request id or timestamp')
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


# # GET request 
# # @GET: Fetch all records from a user after a sent timestamp
# @requests_api.route('/all/<int:id>', methods=['GET'])
# def get_latest_time(id):
#     try:
#         connection = mysql.connect()
#         cursor = connection.cursor(pymysql.cursors.DictCursor)
#         cursor.execute("SELECT * FROM requests WHERE plant_id = %s", id)
#         rows = cursor.fetchall()
#         response = jsonify(rows)
#         return response
#     except:
#         print('Could not FETCH request id or timestamp')
#     finally: 
#         connection.close()
#         cursor.close()