#! env/bin/activate

# Authors: Jayson Tan and Daniel Mallia
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

# POST a plant
@plants_api.route('/insert', methods=['POST'])
def add_plant(userEmail, userName, species, uri, currPhoto):
    # grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO plants(user_email, plant_name, species, uri, curr_photo, date_created) VALUES (%s, %s, %s, %s, %s, %s)"
    recordTuple = (userEmail, userName, species, uri, currPhoto, now)
    # DL: recordTuple = ('agentsmith@aol.com', 'perry the platypus', 'snake-tree', 'http://sample.com/', 3, now)

    try:
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)

        # insert a plant into `plants` table
        cur.execute(sqlQuery, recordTuple)

        # commit changes to database so new record persists
        connection.commit()
        return "OK"

    except:
        print('Could not add a plant')
        return "Not OK"
    finally:
        connection.close()
        cur.close()

# GET all plants from 'plant_info'
@plants_api.route('/', methods=['GET'])
def fetch_all_plants():
    try:
        # connect to MySQL instance
        connection = mysql.connect()

        # pymysql cursors that returns results as a dictionary
        # cursor objects allows users to execute queries per row
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM plants")

        # .fetchall() retrieves a JSON object
        rows = cur.fetchall()

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
        cur.close()

        # DELETE a plant


# @plants_api.route('/plant/<int:id>', methods=['DELETE'])
# def delete_plant(id):
#     try:
#         connection = mysql.connect()
#         cur = connection.cursor(pymysql.cursors.DictCursor)
#         cur.execute("DELETE FROM plants WHERE plant_id = %s", id)
#         connection.commit()
#         return "OK"
#     except:
#         print('Could not delete plant')
#     finally:
#         connection.close()
#         cur.close()


# GET a plant identified by 'id' using FLask's converter to specify argument type, <CONVERTER:VARIABLE_NAME>
@plants_api.route('/plant/<int:id>', methods=['GET', 'DELETE'])
def fetch_plant(id):
    if request.method == 'GET':
        try:
            connection = mysql.connect()
            cur = connection.cursor(pymysql.cursors.DictCursor)

            # query for a single plant matching 'id', %s is a placeholder of string type
            cur.execute("SELECT * FROM plants WHERE plant_id = %s", id)
            single_plant = cur.fetchone()
            response = jsonify(single_plant)

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
            cur.close()
    elif request.method == 'DELETE':
        try:
            connection = mysql.connect()
            cur = connection.cursor(pymysql.cursors.DictCursor)
            cur.execute("DELETE FROM plants WHERE plant_id = %s", id)
            connection.commit()
            return "OK"
        except:
            print('Could not delete plant')
        finally:
            connection.close()
            cur.close()
    else: 
        return "Nothing"

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
