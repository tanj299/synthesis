#! env/bin/activate

# Authors: Jayson Tan 
# File: main.py
# Date Begun: 03/25/2020
# Last Updated: 04/04/2020
# Driver application of the REST API
# Note: Consider looking into dotenv to set flask app variables without having to set it in the terminal every time


import os 
from flask import Flask, render_template, redirect, url_for, session
from extensions import mysql
from flask_login import LoginManager

from plants import plants_api
from configuration import config_api
from login import login_api

# Flask application
app = Flask(__name__)

# mysql config
app.config['SECRET_KEY'] = 'synthesizeMeCaptain'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'synthesize0220'
app.config['MYSQL_DATABASE_DB'] = 'synthesis'
app.config['MYSQL_DATABASE_HOST'] = 'synthesis-database.c0a8ellxvhhd.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

# Register Blueprint objects with the application to modularize our code 
app.register_blueprint(plants_api, url_prefix = "/plants")
app.register_blueprint(config_api, url_prefix = "/config")
app.register_blueprint(login_api, url_prefix = "/login")

# Index route; test backend
@app.route('/')
def index():
    return('Welcome to the backend!')

# Initialize Flask-Login immediately after app
login = LoginManager(app)

# __name__ == current file running directly, which IS "__main__"
# If main.py is imported to another file, then it is NOT "__main__" 
# __name__ will be set to the file that the other file is named
if __name__ == "__main__":
    app.run()
