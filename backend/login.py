#! env/bin/activate

# Authors: Jayson Tan
# File: login.py
# Date Begun: 04/16/2020
# Last Updated: 04/16/2020

# Implementation of REST API routes via Python Flask and pymysql
# Routes for logging users 

import pymysql
import time
from extensions import mysql
from flask import jsonify, Flask, flash, request, Blueprint, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

# Werkzeug library used to verify user password matches with the DB password
# Flask-Login extension manages login state and user sessions

# Blueprint object for login
login_api = Blueprint('login_api', __name__)

@login_api.route('/test')
def index():
    return('Welcome to login!')

# @login_api.route('/', methods=['GET', 'POST'])
# def login():

    
