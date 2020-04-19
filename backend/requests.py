#! env/bin/activate

# Authors: Jayson Tan
# File: requests.py
# Date Begun: 03/25/2020
# Last Updated: 04/16/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for configuring the initial Raspberry Pi

import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

requests_api = Blueprint('requests_api', __name__)

@requests_api.route('/')
def index():
    return('Welcome to requests!')


# @requests_api('/<int:id>')
# query to select the latest request from a user:
# select t1.* from requests t1 where t1.timestamp = (select max(t2.timestamp) from requests t2 where t2.plant_id=t1.plant_id) having plant_id = 2
