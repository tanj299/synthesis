#! env/bin/activate

# Authors: Jayson Tan
# File: main.py
# Date Begun: 04/26/2020
# Last Updated: 04/26/2020
# Flask-Login user class

from flask import Flask 
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self):
        self.id = None
        self.username = None 
        self.email = None 
        self._is_authenticated = False 
        self._is_active = True
        self._is_anonymous = False 

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, val):
        self._is_authenticated = val

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, val):
        self._is_active = val 

    @property 
    def check_password(self, request_password, password):
        if request_password:
            self.is_authenticated = request_password == str(password)
        else:
            self.is_authenticated = False 