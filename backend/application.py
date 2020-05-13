#! env/bin/activate

# Authors: Jayson Tan 
# File: main.py
# Date Begun: 03/25/2020
# Last Updated: 04/25/2020
# Driver application of the REST API
# Note: Consider looking into dotenv to set flask application variables without having to set it in the terminal every time
# DL: Delete later, used for testing purposes
# https://github.com/maxcountryman/flask-login
# https://codereview.stackexchange.com/questions/110679/simple-login-system-using-python-flask-and-mysql
# https://flask-login.readthedocs.io/en/latest/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions


import os 
from flask import Flask, render_template, redirect, url_for, session, request
from flask_login import LoginManager, UserMixin, login_required
from extensions import mysql

from plants import plants_api
from configuration import config_api
from login import login_api
from make_requests import requests_api
from logs import logs_api
from alert import alert_api

# Flask application
# DL: secret key
application = Flask(__name__)
application.secret_key = 'secret_test'

# mysql config
application.config['SECRET_KEY'] = 'synthesizeMeCaptain'
application.config['MYSQL_DATABASE_USER'] = 'admin'
application.config['MYSQL_DATABASE_PASSWORD'] = 'synthesize0220'
application.config['MYSQL_DATABASE_DB'] = 'synthesis'
application.config['MYSQL_DATABASE_HOST'] = 'synthesis-database.c0a8ellxvhhd.us-east-1.rds.amazonaws.com'
mysql.init_app(application)

# Register Blueprint objects with the application to modularize our code 
application.register_blueprint(plants_api, url_prefix = "/plants")
application.register_blueprint(config_api, url_prefix = "/config")
application.register_blueprint(login_api, url_prefix = "/login")
application.register_blueprint(requests_api, url_prefix = "/requests")
application.register_blueprint(logs_api, url_prefix = "/logs")
application.register_blueprint(alert_api, url_prefix = "/alert")

# Initialize Flask-Login immediately after application
login = LoginManager(application)

# Index route; test backend
@application.route('/')
def index():
    return('Welcome to the backend!')

# __name__ == current file running directly, which IS "__main__"
# If main.py is imported to another file, then it is NOT "__main__" 
# __name__ will be set to the file that the other file is named
if __name__ == "__main__":
    application.run(host='0.0.0.0')
