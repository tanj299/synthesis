#! env/bin/activate

# Authors: Jayson Tan
# File: make_requests.py
# Date Begun: 04/19/2020
# Last Updated: 04/30/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for making requests to the Raspberry Pi


import time
import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

requests_api = Blueprint('requests_api', __name__)

# @Dan, if you want to double check for sanity's sake I wrote a script in the folder, 'test_api' in the file, 'test.py' 
# Otherwise, this is just a cleaner version of the same function 
def convert_time_format(date):
    date_parse = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_converted = datetime.strftime(dateT, "%Y-%m-%d+%H%%3A%M%%3A%S")
    return date_converted

@requests_api.route('/')
def index():
    return('Welcome to requests!')

# POST request
# @POST: Create a request to affect the sensors
# @category: Three valid categories: water, light, and picture
@requests_api.route('/insert', methods=['POST'])
def post_latest():

    # Grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    plant_id = request.json['plant_id']
    timestamp = request.json['timestamp']
    category = request.json['category']

    # Check `category` is valid; else return
    if category != 'water' and category != 'light' and category != 'picture':
        print("Incorrect category - please choose 'water', 'light', or 'picture'")
        return

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
        "category": "water"
    }
    '''

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO make_requests(plant_id, category, timestamp) VALUES (%s, %s, %s)"
    recordTuple = (plant_id, category, now)

    data = {"plant_id": plant_id,
            "timestamp": now,
            "category": category
            }

    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sqlQuery, recordTuple)

        # Commit record to database so new record persists
        connection.commit()
        return jsonify(data)
    except:
        print('Could not POST a new request')
        return('Request failed: ensure that the plant exists and the plant_id matches with the `plants` table or category is valid')
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
        cursor.execute("SELECT t1.* FROM make_requests AS t1 WHERE t1.timestamp = (SELECT MAX(t2.timestamp) FROM make_requests AS t2 WHERE t2.plant_id = t1.plant_id) HAVING plant_id = %s", id)
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
