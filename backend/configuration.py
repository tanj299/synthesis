#! env/bin/activate

# Authors: Jayson Tan 
# File: configuration.py
# Date Begun: 03/25/2020
# Last Updated: 04/10/2020


# Implementation of REST API routes via Python Flask and pymysql
# Routes for configuring the initial Raspberry Pi 

import pymysql
import time 
from extensions import pymysql
from flask import Flask, request, jsonify, Blueprint

config_api = Blueprint('config_api', __name__)

@config_api.route('/')
def index():
    return('Welcome to config!')

if __name__ == ('main'):
    app.run(debug=True)
