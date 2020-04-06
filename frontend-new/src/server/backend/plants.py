#! env/bin/activate

# Authors: Jayson Tan 
# File: plants.py
# Date Begun: 03/25/2020
# Last Updated: 04/04/2020

# Implementation of REST API routes via Python Flask and SQLAlchemy 
# Routes for CRUD operations on `plants` table 
# Use Postman to test routes and endpoints
# pymysql allows us to query with SQL statements
# Note: python3 does NOT support flask-mysqldb
# DL: Delete Later, used for testing, remove during production

import pymysql
import time
from extensions import mysql
from flask import jsonify, Flask, flash, request, Blueprint
# from werkzeug import generate_password_hash, check_password_hash

plants_api = Blueprint('plants_api', __name__)

# POST request
# @POST: create a plant with id autoincremented in the database
@plants_api.route('/insert', methods=['POST'])
def add_plant():
    # grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    # request.json sends a JSON body attached to the request, check with POSTMAN
    # POSTMAN requirements: HEADERS: Key: Content-Type, Value: application/json
    # sample body: 
    '''
    {
        "user_email": "bobbylee@gmail.com",
        "plant_name": "bobby",
        "species": "orchid",
        "uri": "http://sampleokay.com",
        "curr_photo": 99
    }
    '''

    user_email = request.json['user_email']
    plant_name = request.json['plant_name']
    species = request.json['species']
    uri = request.json['uri']
    currPhoto = request.json['curr_photo']

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO plants(user_email, plant_name, species, uri, curr_photo, date_created) VALUES (%s, %s, %s, %s, %s, %s)"
    recordTuple = (user_email, plant_name, species, uri, currPhoto, now)
    # DL: recordTuple = ('agentsmith@aol.com', 'perry the platypus', 'snake-tree', 'http://sample.com/', 3, now)

    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # insert a plant into `plants` table
        cursor.execute(sqlQuery, recordTuple)

        # commit changes to database so new record persists
        connection.commit()
        return jsonify("OK")

    except:
        print('Could not add a plant')
        return jsonify("Not OK")
    finally:
        connection.close()
        cursor.close()

# GET request
# @GET: fetch all plants from 'plants' table
@plants_api.route('/', methods=['GET'])
def fetch_all_plants():
    try:
        # connect to MySQL instance
        connection = mysql.connect()

        # pymysql cursors that returns results as a dictionary
        # cursor objects allows users to execute queries per row
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM plants")

        # .fetchall() retrieves a JSON object
        rows = cursor.fetchall()

        # creates a response with the JSON representation
        response = jsonify(rows)
        response.status_code = 200

        # return response as a JSON object
        return response
    except:
        print('An exception occurred')
    finally:
        # close the MySQL instance and cursor object when done
        connection.close()
        cursor.close()


# GET, DELETE requests
# a plant is identified by 'id' using Flask's converter to specify argument type, <CONVERTER:VARIABLE_NAME>
# @GET: return a plant's information matching the ide from the database
# @DELETE: remove plant matching the id from the database
@plants_api.route('/plant/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def fetch_plant(id):
    if request.method == 'GET':
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # query for a single plant matching 'id', %s is a placeholder of string type
            cursor.execute("SELECT * FROM plants WHERE plant_id = %s", id)
            single_plant = cursor.fetchone()
            response = jsonify(single_plant)
            print(response)

            # if plant_id is not found, error 404
            if single_plant == None:
                print('Could not fetch plant with id', id)
                response.status_code = 404

            # else, plant_id is found, return response object
            else:
                response.status_code = 200
                
            return response
        except: 
            print('Could not fetch a plant with id')
        finally:
            connection.close()
            cursor.close()
    elif request.method == 'DELETE':
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("DELETE FROM plants WHERE plant_id = %s", id)
            connection.commit()
            return "OK"
        except:
            print('Could not delete plant')
        finally:
            connection.close()
            cursor.close()
    else: 
        return "Nothing"

# PUT request
# @PUT: update a plant's information matching the id from the database
@plants_api.route('/update/<int:id>', methods=['PUT'])
def update_plant(id):
    try:
        user_email = request.json['user_email']
        plant_name = request.json['plant_name']
        species = request.json['species']
        uri = request.json['uri']
        curr_photo = request.json['curr_photo']

        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        recordTuple = (user_email, plant_name, species, uri, curr_photo, id)
        sqlQuery = "UPDATE plants SET user_email=%s, plant_name=%s, species=%s, uri=%s, curr_photo=%s WHERE plant_id=%s"
        # DL: dummy = ('bloop@yahoo.com', 'caroline', 'sunflower', 'http://notasample.com', 8, id)
        # DL: sqlQuery = "UPDATE plants SET user_email='johnsmith@yahoo.com', plant_name='mira', species='rose', uri='http://totallyasample.com', curr_photo=16 WHERE plant_id=%s"

        cursor.execute(sqlQuery, recordTuple)
        connection.commit()
        response = jsonify('Plant updated successfully!')
        return response
    except:
        return jsonify('Not found')
    finally:
        connection.close()
        cursor.close()

# HTTP response with 404 error 
@plants_api.errorhandler(404)
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
