#! /usr/bin/env python3

# Authors: Daniel Mallia and Jayson Tan
# Date Begun: 3/14/2020

# This is the Python script intended to run on a Raspberry Pi and serve as
# the guiding "brain" of a synthesis garden's operation. It is called 
# garden_driver for this reason as well as because it acts as a software 
# driver, communicating with the actual hardware components.

import sys, time
import serial
import requests
from pynput import keyboard

# GLOBALS
run_program=True
plants = {}     # Addresses Plant instances by plant ID (integer)
arduinos = {}   # Address arduinos (Serial objects) by port name (string)

class Plant():
	def __init__(self, name, id, arduino, position):
		self.name = name
		self.id = id
		
		if(arduino in arduinos):
			self.arduino = arduinos[arduino]
		else:
			arduinos[arduino] = serial.Serial(arduino, timeout=10)
			self.arduino = arduinos[arduino]

		self.position = position

		# Initialize soil temp sensor
		if(self.position == '1'):
			self.arduino.write(b'4')
		else:
			self.arduino.write(b'5')

	def water(self):
		self.arduino.write(b'8')
		time.sleep(5)
		self.arduino.write(b'9')

	def get_info(self):
		self.arduino.write(self.position.encode(encoding="ascii"))
		data = self.arduino.readline()
		return data

# Keyboard listener callback
# If the user presses q, change run_program to False
def on_press(key):
	global run_program

	if(hasattr(key,'char') and key.char == 'q'):
		run_program = False
		return False # Stop listener

	return True # Do not stop listener


# Function to print greeting screen, request login information and authorize 
# (acquire API access token)
def greet_and_login():
	# Greeting screen
	line = ('*' * 80) + '\n'
	blank = ' ' * 30
	print(line, line, '\n', blank, 'Welcome to SYNTHESIS', blank, '\n\n', line,
		line, 'Created by Leo Au-Yeung, Stanley Lim, Daniel Mallia and Jayson',
			'Tan\nHunter College, Spring 2020\n\n', sep ='')

	# Check library versions:
	print("Python version: ", sys.version)
	print("Serial library version: ", serial.__version__, "\n\n")

	# Request login information
	email = input('Enter your account email: ')
	password = input('Enter your account password: ')

	# Authorize - EXPAND TO CHECKING LOOP WHEN AUTHORIZATION SET UP
	token = ''

	print("Press q to quit the program.")

	return email, token

# Check user configuration and update script accordingly
# Returns true/false to enable different behavior in response to failed
# communication.
def configure(email):
	r = requests.get("http://127.0.0.1:5000/plants/all/" + email + "/")

	if(r.status_code != 200):
		print("Could not retrieve user configuration.")
		return False
	else:
		for entry in r.json():
			id = entry["plant_id"]
			if(id not in plants):
				name = entry["plant_name"]
				port = entry["serial_port"]
				position = str(entry["position"])
				plants[id] = Plant(name, id, port, position)
				print("Added plant: " + name)

	return True

# Function to cleanly exit the program
def cleanup():
	print("Stopping...")

	# Close all Serial connections
	for arduino in arduinos:
		arduinos[arduino].close()

	print("Please reset and unplug your arduinos!")

def main():
	global run_program

	# Greet
	email, token = greet_and_login()

	# Set up listener for quit command
	listener = keyboard.Listener(on_press=on_press)
	listener.start()

	# Read in user configuration - loop while not successful
	while(not configure(email)):
		time.sleep(5)

	minute_tracker = time.time()
	hour_tracker = time.time()
	query_time = time.strftime("%Y-%m-%d %H:%M:%S")

	# Primary Loop:
	while(run_program):
		# 1. Read the database control table
		# 		If error in read, set errorDatabase, and e-mail user
		# 		Else set command flags (Raspberry Pi)
		# 2. Process command flags
		# 		If dataNow - write average of existing saved values to table
		# 		If lightNow - turn on light
		# 		Etc. (Including checks that these were met - lightNow yields 
		# 			actual light on and such)

		for plant in plants:	
			r = requests.get("http://127.0.0.1:5000/requests/all/" + str(plant) 
				+ "/" + query_time)
			
			watered = False
			for req in r.json(): 
				if(req['category'] == "water" and watered == False):
					plants[plant].water()
					watered = True

		query_time = time.strftime("%Y-%m-%d %H:%M:%S")

		# 3. Data logging:
		# 		If greater than 60 seconds - collect value (may want to poll 
		# 			now, get value on next loop)
		# 		If greater than 60 minutes - write average to database
		if(time.time() - minute_tracker >= 60):
			minute_tracker = time.time()

		if(time.time() - hour_tracker >= 3600):
			hour_tracker = time.time()
		
		# 4. Process automated aspects:
		# 		Water if low moisture
		# 		Light if low light (and not night time)
		# 		etc.

		time.sleep(10)

	cleanup()

if __name__ == '__main__':
	main()
