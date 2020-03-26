#! #! env/bin/activate

# Authors: Jayson Tan and Daniel Mallia
# Date Begun: 03/25/2020

# This is the Python config file for Amazon AWS RDS MySQL instance
# We initialize a flask extension to access a MySQL database 
# app.config[''] is used to configure access to MySQL database server

from app import app
from flaskext.mysql import MySQL 

mysql = MySQL()

# mysql config
app.config['MYSQL_DATABASE_USER'] = 'admin' 
app.config['MYSQL_DATABASE_PASSWORD'] = 'synthesize0220'
app.config['MYSQL_DATABASE_DB'] = 'autogarden'
app.config['MYSQL_DATABASE_HOST'] = 'synthesis-database.c0a8ellxvhhd.us-east-1.rds.amazonaws.com'
mysql.init_app(app)
