#! /usr/bind/env_python3

# Authors: Jayson Tan and Daniel Mallia
# Date Begun: 03/18/2020

# This is the Python script intended to connect to the AWS RDS instance, synthesis-database
# The database will be the backend and the endpoint for both the frontend portion 
# of this project (our React-Native app as well as our Web app)
# as well as the hardware portion, the Raspberry Pi and Arduino

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# engine class connects a pool and dialect together to provide a source of database connectivity
# instantiate an engine object using `create_engine()`
engine = create_engine("mysql+pymysql://admin:synthesize0220@synthesis-database.c0a8ellxvhhd.us-east-1.rds.amazonaws.com/autogarden", echo = True)
connection = engine.connect()
result = connection.execute('SELECT device_name FROM controller;')

Base = declarative_base()

# MetaData contains definitions of tables and associated objects
meta = MetaData()

# example table creation
arduino = Table('arduino', meta,
    Column('id', Integer, primary_key=True),
    Column('sensor_name', String(60), nullable=False),
    Column('output', Boolean, unique=False, default=True)
)

arduino.create(engine)

for row in result:
    print("device_name: ", row['device_name'])

connection.close() 

