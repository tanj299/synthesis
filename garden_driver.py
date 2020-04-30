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


# Key Global Structures 
plants = {}		# Addresses Plant instances by plant ID (integer)
arduinos = {}	# Address arduinos (Serial objects) by port name (string)

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

	# Authorize 
	token = ''

	return token

def parse_configuration():
	pass

def main():
	# Define universal flags
	connection_error = False

	# TEST ADD SINGLE PLANT
	plants[1] = Plant("Bob", 1, "/dev/ttyACM0", '1')
	
	minute_tracker = time.time()
	hour_tracker = time.time()
	# Primary Loop:
	while(True):
		# 1. Read the database control table
		# 		If error in read, set errorDatabase, and e-mail user
		# 		Else set command flags (Raspberry Pi)
		# 2. Process command flags
		# 		If dataNow - write average of existing saved values to table
		# 		If lightNow - turn on light
		# 		Etc. (Including checks that these were met - lightNow yields 
		# 			actual light on and such)

		# TEST READ SINGLE INSTRUCTION
		for plant in plants:
			r = requests.get("http://127.0.0.1:5000/requests/" + str(plant))
			
			if(r.json()['make_request'] == 1):
				plants[plant].water()


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

if __name__ == '__main__':
	main()
