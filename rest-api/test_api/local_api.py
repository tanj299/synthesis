#! env/bin/activate

# Authors: Jayson Tan and Daniel Mallia
# Date Begun: 03/23/2020

# Implementation of REST APIs 
# At this point, we are able to perform CRUD operations only
# Note: python3 does NOT support flask-mysqldb 

from app import app
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow # for json object serialization/deserialization
import os  

# init app 
app = Flask(__name__)

# set SQLAlchemy DB URI; let server know where the database route is
# os.path.dirname takes current file which is the base directory (__file__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

######################################## class instantiation ########################################

# plant class/model
class Plant(db.Model):
    plant_id = db.Column(db.Integer, primary_key=True)
    moisture_level = db.Column(db.Float)
    humidity_level = db.Column(db.Float)
    light_intensity = db.Column(db.Float)
    is_alive = db.Column(db.Boolean)
    name = db.Column(db.String(128), unique=True)

    # constructor
    def __init__(self, moisture_level, humidity_level, light_intensity, is_alive, name): 
        self.moisture_level = moisture_level
        self.humidity_level = humidity_level
        self.light_intensity = light_intensity
        self.is_alive = is_alive
        self.name = name

# plant schema
class PlantSchema(ma.Schema): 
    class Meta: 
        fields = ('plant_id', 'moisture_level', 'humidity_level', 'light_intensity', 'is_alive', 'name')

# init schema
plant_schema = PlantSchema()

# fetching multiple/list of data
plants_schema = PlantSchema(many = True)


######################################## routes ########################################
# format: @app.route('<ENDPOINT>', methods=['<REQUEST_TYPE>'])

# default path
@app.route('/', methods=['GET'])
def hello():
    return jsonify("Hello, you've reached the backend")

# create a plant
@app.route('/plant', methods=['POST'])
def add_plant():
    moisture_level = request.json['moisture_level']
    humidity_level = request.json['humidity_level']
    light_intensity = request.json['light_intensity']
    is_alive = request.json['is_alive']
    name = request.json['name']

    # instantiate object
    new_plant = Plant(moisture_level, humidity_level, light_intensity, is_alive, name)

    # add to session for storage
    db.session.add(new_plant)

    # commit changes to database so it persists
    db.session.commit()

    return plant_schema.jsonify(new_plant)

# get all plants
@app.route('/plant', methods=['GET'])
def get_plants():
    all_plants = Plant.query.all()
    # after marshmallow upgrade to 3.0+, 'dump' returns the data, so we don't need a '.data' object after 'result'
    result = plants_schema.dump(all_plants)
    return jsonify(result)

# get a plant
@app.route('/plant/<id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    return plant_schema.jsonify(plant)

# update a plant
@app.route('/plant/<id>', methods=['PUT'])
def update_plant(id):
    # first fetch the plant
    plant = Plant.query.get(id)

    # all properties of the plant
    moisture_level = request.json['moisture_level']
    humidity_level = request.json['humidity_level']
    light_intensity = request.json['light_intensity']
    is_alive = request.json['is_alive']
    name = request.json['name']

    # updated properties of a plant
    plant.moisture_level = moisture_level
    plant.humidity_level = humidity_level
    plant.light_intensity = light_intensity
    plant.is_alive = is_alive
    plant.name = name

    db.session.commit()

    return plant_schema.jsonify(plant)

# delete a plant
@app.route('/plant/<id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    db.session.delete(plant)
    db.session.commit()

    return plant_schema.jsonify(plant)

# @app.route('/', methods = ['GET'])
# def get():
#     return jsonify({'msg': 'Hello World'})

# run server
if __name__ == '__main__':
    app.run(debug=True)
