#! env/bin/activate

# Authors: Jayson Tan
# File: logs.py
# Date Begun: 04/19/2020
# Last Updated: 04/19/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for logging information to the database from Raspberry Pi

import time
import pymysql
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

logs_api = Blueprint('logs_api', __name__)

@logs_api.route('/')
def index():
    return('Welcome to logs!')

# @logs_api.route('/fetch')