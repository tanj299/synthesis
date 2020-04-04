#! env/bin/activate

# Authors: Jayson Tan and Daniel Mallia
# File: main.py
# Date Begun: 03/25/2020
# Last Updated: 04/04/2020
# Main implementation of the REST API

# Flask application 

from flask import Flask
from extensions import mysql
from plants import plants_api

app = Flask(__name__)

# mysql config
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'synthesize0220'
app.config['MYSQL_DATABASE_DB'] = 'synthesis'
app.config['MYSQL_DATABASE_HOST'] = 'synthesis-database.c0a8ellxvhhd.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

# register Blueprint with the application for response 
# here we utilize Blueprint to modularize our code 
app.register_blueprint(plants_api, url_prefix = "/plants")

# welcome to backend
@app.route('/')
def welcome():
    return('Welcome to the backend!')


if __name__ == "__main__":
    app.run()
