#! env/bin/activate

# Authors: Jayson Tan 
# File: main.py
# Date Begun: 03/25/2020
# Last Updated: 04/04/2020
# Driver application of the REST API
# Note: Consider looking into dotenv to set flask app variables without having to set it in the terminal every time
# DL: Delete later, used for testing purposes
# https://github.com/maxcountryman/flask-login
# https://codereview.stackexchange.com/questions/110679/simple-login-system-using-python-flask-and-mysql
# https://flask-login.readthedocs.io/en/latest/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions


import os 
import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# from flask import Flask, render_template, redirect, url_for, session, request
from extensions import mysql
# from flask_login import LoginManager, UserMixin, login_required

from plants import plants_api
from configuration import config_api
# from login import login_api
from requests import requests_api
from logs import logs_api

# Flask application
# DL: secret key
app = Flask(__name__)
app.secret_key = 'secret_test'

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
# app.register_blueprint(login_api, url_prefix = "/login")
app.register_blueprint(requests_api, url_prefix = "/requests")
app.register_blueprint(logs_api, url_prefix = "/logs")

# # Index route; test backend
# @app.route('/')
# def index():
#     return('Welcome to the backend!')


####### TEST #######

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
# Our mock database.
users = {'foo@bar.tld': {'password': 'secret'}}


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

# Index route; test backend
@app.route('/')
def index():
    return('Welcome to the backend!')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


# __name__ == current file running directly, which IS "__main__"
# If main.py is imported to another file, then it is NOT "__main__" 
# __name__ will be set to the file that the other file is named
if __name__ == "__main__":
    app.run()
