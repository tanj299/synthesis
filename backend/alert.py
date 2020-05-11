#! env/bin/activate

# Authors: Jayson Tan
# File: alert.py
# Date Begun: 05/11/2020
# Last Updated: 05/11/2020

# Implementation of REST API routes via Python Flask and pymysql
# Functions for sending emails


import smtplib, ssl
import pymysql
import socketserver
from extensions import mysql
from flask import jsonify, Flask, request, Blueprint

alert_api = Blueprint('alert_api', __name__)

# Create a secure SSL context
# Port 465 is used for SMTP; other ports are 25 and 587
port = 465
smtp_server = "smtp.gmail.com"
sender_email = "synthesis.creators@gmail.com"
password = "synthesize0220"

@alert_api.route('/<int:id>/<alert_message>', methods=['GET'])
def alert(id, alert_message): 
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT user_email FROM plants WHERE plant_id=%s", id)
        single_plant = cursor.fetchone()
        response = jsonify(single_plant)

        # Get receiver's email based on their plant_id
        receiver_email = response.get_data(as_text=True)

        if alert_message == "water":
            message = """From: From Synthesis Admins <synthesis.creators@gmail.com>
            Subject: Synthesis - Water Tank Low

            Your water tank is running low. Consider refilling your water tank
            """

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

        elif alert_message == "new":
            message = """From: From Synthesis Admins <synthesis.creators@gmail.com>
            Subject: Synthesis - New Plant Added

            Congrats on your new plant!
            """

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

        return response
    except:
        return('Request failed: ensure that the plant exists and the plant_id matches with the `plants` table')
    finally: 
        connection.close()
        cursor.close()

