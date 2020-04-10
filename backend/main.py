#! env/bin/activate

# Authors: Jayson Tan 
# File: main.py
# Date Begun: 03/25/2020
# Last Updated: 04/04/2020
# Driver application of the REST API
# Note: Consider looking into dotenv to set flask app variables without having to set it in the terminal every time


from flask import Flask
from extensions import mysql
from plants import plants_api

# Flask application
app = Flask(__name__)

# mysql config
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'synthesize0220'
app.config['MYSQL_DATABASE_DB'] = 'synthesis'
app.config['MYSQL_DATABASE_HOST'] = 'synthesis-database.c0a8ellxvhhd.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

# Register Blueprint with the application for response 
# Here we utilize Blueprint to modularize our code 
app.register_blueprint(plants_api, url_prefix = "/plants")

# Index route; test backend
@app.route('/')
def index():
    return('Welcome to the backend!')

if __name__ == "__main__":
    app.run()
