#! env/bin/activate

# Authors: Jayson Tan 
# File: extensions.py
# Date Begun: 03/25/2020
# Last Updated: 04/02/2020

# Required to use Blueprint objects to modularize our code, otherwise, we have circular dependencies 
# For more information, here's the documentation and common way to use Blueprint: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint
# https://stackoverflow.com/questions/28784849/how-to-fix-circular-import-in-flask-project-using-blueprints-mysql-w-o-sqlalchem

from flaskext.mysql import MySQL

mysql = MySQL()
