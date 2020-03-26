#! env/bin/activate

# Authors: Jayson Tan and Daniel Mallia
# Date Begun: 03/25/2020

# Implementation of REST API routes via Python Flask and SQLAlchemy 
# At this point, we are able to perform CRUD operations 
# Use Postman to test routes and endpoints
# pymysql allows us to query with SQL statements
# Note: python3 does NOT support flask-mysqldb

import pymysql
from app import app
from rds_config import mysql
from flask import jsonify
from flask import flash, request
# from werkzeug import generate_password_hash, check_password_hash

# welcome to backend
@app.route('/')
def welcome(): 
    return('Welcome to the backend!')

# GET all plants from 'plant_info'
@app.route('/plant', methods=['GET'])
def fetch_all_plants():
    try:
        # connect to MySQL instance
        connect = mysql.connect()
        cur = connect.cursor(pymysql.cursors.DictCursor)
        # pymysql cursors that returns results as a dictionary
        # cursor objects allows users to execute queries per row
        cur.execute("SELECT * FROM plant_info")

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
        connect.close()
        cur.close()

# GET a plant identified by 'id'
@app.route('/plant/<id>', methods=['GET'])
def fetch_plant(id):
    try:
        connect = mysql.connect()
        cur = connect.cursor(pymysql.cursors.DictCursor)

        # query for a single plant matching 'id', %s is a placeholder of string type
        cur.execute("SELECT * FROM plant_info WHERE plant_id = %s", id)
        single_plant = cur.fetchone()
        response = jsonify(single_plant)

        # if plant_id is not found, error 404
        if single_plant == None:
            print('Could not fetch plant with id', id)
            response.status_code = 404
            return response

        # else, plant_id is found, return response object
        else:
            response.status_code = 200
            return response
    except: 
        print('Could not fetch a plant with id')
    finally:
        connect.close()
        cur.close()

# HTTP response with 404 error 
@app.errorhandler(404)
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
