#! env/bin/activate

# Authors: Jayson Tan
# File: requests.py
# Date Begun: 03/25/2020
# Last Updated: 04/16/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for configuring the initial Raspberry Pi

import time
import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

requests_api = Blueprint('requests_api', __name__)

request
@requests_api.route('/')
def index():
    return('Welcome to requests!')

# query to select the latest request from a user:
# select t1.* from requests t1 where t1.timestamp = (select max(t2.timestamp) from requests t2 where t2.plant_id=t1.plant_id) having plant_id = 2
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
        return response 
    except:
        print('Could not FETCH request id')
    finally: 
        connection.close()
        cursor.close()


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

    # POSTMAN requirements: HEADERS: Key: Content-Type, Value: application/json
    # Note: "timestamp" field should be an empty string since backend Python will take care of datetime 
    # Sample body:
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
    
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Insert request into `requests` table
        # Pass sqlQuery and recordTuple as arguments
        cursor.execute(sqlQuery, recordTuple)

        # Commit record to database so new record persists
        connection.commit()
        return jsonify("OK")
    except:
        print('Could not POST a new request')
        return('Request failed: ensure that the plant exists and the plant_id matches with the `plants` table')
    finally:
        connection.close()
        cursor.close()


if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Execute `flask run` instead")
