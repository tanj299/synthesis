#! env/bin/activate

# Authors: Jayson Tan
# File: main.py
# Date Begun: 04/26/2020
# Last Updated: 04/26/2020
# Flask User class 

from flask import Flask
from flask_login import UserMixin

class User():

    def __init__(self): 
        self.id = id 
        self.username = None 
        self.password = None   
        self.is_logged_in = False 