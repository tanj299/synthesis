#! env/bin/activate

# Authors: Jayson Tan
# File: plants.py
# Date Begun: 03/25/2020
# Last Updated: 04/20/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for CRUD operations on `plants` table
# Use Postman to test routes and endpoints
# pymysql allows us to query with SQL statements
# Note: python3 does NOT support flask-mysqldb
# DL: Delete Later, used for testing, remove during production


import pymysql
import time
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint, json
# from werkzeug import generate_password_hash, check_password_hash

plants_api = Blueprint('plants_api', __name__)

# Split useremail at the '@' symbol 
# Ex: janesmith@gmail.com -> janesmith
def email_to_uri(email):
    name = email.split("@")[0]
    uri = 'https://elasticbeanstalk-us-east-1-813224974598.s3.amazonaws.com/photos/' + name +'.png'
    return uri

# Index route for 'plants'
# route() is a decorator which takes the function plant_index() as an argument
# For instance, this function translates to:
# plant_index() = plants_api.route('/', plant_index, <OPTIONS> )
@plants_api.route('/')
def plant_index():
    return ('Welcome to plants!')

# POST request
# @POST: Create a plant with id autoincremented in the database
@plants_api.route('/insert', methods=['POST'])
def add_plant():
    # Grab current time in mysql datetime format
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    # request.json sends a JSON body attached to the request, check with POSTMAN
    user_email = request.json['user_email']
    plant_name = request.json['plant_name']
    species = request.json['species']
    curr_photo = request.json['curr_photo']
    serial_port = request.json['serial_port']
    position = request.json['position']
    water_threshold = request.json['water_threshold']
    light_threshold = request.json['light_threshold']

    # Reformat the user email to the photo uri
    uri = email_to_uri(user_email)
    
    # POSTMAN requirements:
    '''
    HEADERS: Key: Content-Type, Value: application/json
    BODY: raw
    '''

    # Sample body:
    '''
    {
        "user_email": "bobbylee@gmail.com",
        "plant_name": "bobby",
        "species": "orchid",
        "uri": "https://elasticbeanstalk-us-east-1-813224974598.s3.amazonaws.com/photos/janesmith.png"
        "curr_photo": 99, 
        "water_threshold": 50, 
        "light_threshold": 50
    }
    '''

    # INSERT query and fields to insert
    sqlQuery = "INSERT INTO plants(user_email, plant_name, species, uri, curr_photo, serial_port, position, water_threshold, light_threshold, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    recordTuple = (user_email, plant_name, species, uri, curr_photo, serial_port, position, water_threshold, light_threshold, now)

    # To properly return the JSON data, we put the data into a Python dictionary
    # Then, jsonify() will work properly
    data = {
            "user_email": user_email,
            "plant_name": plant_name, 
            "species": species,
            "uri": uri,
            "curr_photo": curr_photo,
            "serial_port": serial_port,
            "position": position, 
            "water_threshold": water_threshold,
            "light_threshold": light_threshold,
            "date_created": now
            }    
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Insert a plant into `plants` table
        cursor.execute(sqlQuery, recordTuple)

        # Commit changes to database so new record persists
        connection.commit()

        # Return json data after POST request
        return jsonify(data)

    except:
        print('Could not add a plant')
        return jsonify("Not OK")
    finally:
        connection.close()
        cursor.close()

# GET request
# @GET: fetch all plants from 'plants' table
@plants_api.route('/all', methods=['GET'])
def fetch_all_plants():
    try:
        # Connect to MySQL instance
        connection = mysql.connect()

        # pymysql cursors that returns results as a dictionary
        # Cursor objects allows users to execute queries per row
        # Result is stored in the cursor object 
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM plants")

        # .fetchall() retrieves a JSON object from the cursor object
        # Can also use `list(cursor)`, but .fetchall() returns a list OR an empty tuple if list is empty
        rows = cursor.fetchall()

        # Creates a response with the JSON representation
        response = jsonify(rows)
        response.status_code = 200

        # Return response as a JSON object
        return response
    except:
        print('An exception occurred')
    finally:
        # Close the MySQL instance and cursor object when done
        connection.close()
        cursor.close()

# GET request
# @GET: Fetch all plants from 'plants' table associated with email
# Requires a backslash at the end to query with an email
# Ex: janesmith@gmail.com OR janesmith%40gmail.com
@plants_api.route('/all/<string:user_email>/', methods=['GET'])
def fetch_all_plants_email(user_email):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # fetch config match user_email
        cursor.execute(
            "SELECT * FROM plants WHERE user_email = %s", user_email)

        user = cursor.fetchall()
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

# GET, DELETE requests
# A plant is identified by 'id' using Flask's converter to specify argument type, <CONVERTER:VARIABLE_NAME>
# @GET: Return a plant's information matching the 'id' from the database
# @DELETE: Remove plant matching the id from the database
@plants_api.route('/plant/<int:id>', methods=['GET', 'DELETE'])
def fetch_plant(id):
    if request.method == 'GET':
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Query for a single plant matching 'id', %s is a placeholder of string type
            cursor.execute("SELECT * FROM plants WHERE plant_id = %s", id)
            single_plant = cursor.fetchone()
            response = jsonify(single_plant)
            # print (single_plant)

            # If plant_id is not found, error 404
            if single_plant == None:
                print('Could not fetch plant with id', id)
                response.status_code = 404

            # Else, plant_id is found, return response object
            else:
                response.status_code = 200

            # Test to assert that response returned it JSON format
            # assert response.content_type == 'application/json'
            # data = json.loads(response.get_data(as_text=True))
            # assert data['plant_id'] == 2

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
# @PUT: Update a plant's information matching the id from the database
@plants_api.route('/update/<int:id>', methods=['PUT'])
def update_plant(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Query table by the `id` 
        # Return singleRecord and access the JSON data via dictionary pattern likeso in date_created
        cursor.execute("SELECT * FROM plants where plant_id=%s", id)
        singleRecord = cursor.fetchone()
        date_created = singleRecord["date_created"]

        user_email = request.json['user_email']
        plant_name = request.json['plant_name']
        species = request.json['species']
        curr_photo = request.json['curr_photo']
        serial_port = request.json['serial_port']
        position = request.json['position']
        water_threshold = request.json['water_threshold']
        light_threshold = request.json['light_threshold']

        uri = email_to_uri(user_email)

        data = {"user_email": user_email,
                "plant_name": plant_name,
                "species": species,
                "uri": uri,
                "curr_photo": curr_photo,
                "serial_port": serial_port,
                "position": position, 
                "water_threshold": water_threshold,
                "light_threshold": light_threshold,
                "date_created": date_created
                }

        
        recordTuple = (user_email, plant_name, species, uri, curr_photo, serial_port, position, water_threshold, light_threshold, id)
        sqlQuery = "UPDATE plants SET user_email=%s, plant_name=%s, species=%s, uri=%s, curr_photo=%s, serial_port=%s, position=%s, water_threshold=%s, light_threshold=%s WHERE plant_id=%s"
      
        cursor.execute(sqlQuery, recordTuple)
        connection.commit()
        response = jsonify('Plant updated succesfully!', data)
        response.status_code = 200

        return response

    except:
        return ('Not found')
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
else:
    print("Execute `flask run` instead")
