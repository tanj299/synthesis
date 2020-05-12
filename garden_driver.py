#! /usr/bin/env python3

# Authors: Daniel Mallia and Jayson Tan
# Date Begun: 3/14/2020

# This is the Python script intended to run on a Raspberry Pi and serve as
# the guiding "brain" of a synthesis garden's operation. It is called 
# garden_driver for this reason as well as because it acts as a software 
# driver, communicating with the actual hardware components.

import sys, time, argparse
import serial
import requests
from pynput import keyboard
from picamera import PiCamera
from io import BytesIO
import boto3

# GLOBALS
run_program=True
plants = {}     # Addresses Plant instances by plant ID (integer)
arduinos = {}   # Address arduinos (Serial objects) by port name (string)
HOST = "http://backend-dev222222.us-east-1.elasticbeanstalk.com/"
BUCKET = "elasticbeanstalk-us-east-1-813224974598"

class Plant():
	def __init__(self, name, id, arduino, position, water_threshold,
		light_threshold):
		self.name = name
		self.id = id
		
		if(arduino in arduinos):
			self.arduino = arduinos[arduino]
		else:
			try:
				arduinos[arduino] = serial.Serial(arduino, timeout=5)
			except serial.SerialException:
				print("Could not establish connection on port: ", arduino)
				print("Please check that the port name is correct and the ",
					"port is otherwise not in use.")
				cleanup()
			self.arduino = arduinos[arduino]
			time.sleep(10)

		self.position = position
		self.water_threshold = water_threshold
		self.light_threshold = light_threshold
		self.watered_today = False

		# Data
		# Lists are used for averaging values taken over the previous hour
		self.data_dict = {'temp': [], 'humidity': [], 'light': [],
			'soil_moisture': [], 'soil_temp': []}
		self.water_level = False # True = sufficient water
		self.light_on = False

		# Initialize soil temp sensor
		if(self.position == '1'):
			self.arduino.write(b'4')
		else:
			self.arduino.write(b'5')

		response = self.arduino.readline()
		response = response.decode("ascii").rstrip('\r\n')
		if(response == "" or response == "1"):
			print("Could not set up soil temperature sensor for plant: ",
				self.name)

		# Check water level
		self.check_water_level()

	# Returns True if watering was successful, else False
	def water(self):
		self.check_water_level()

		if(self.water_level):
			self.arduino.write(b'8')
			time.sleep(5)
			self.arduino.write(b'9')
			return True
		else:
			print("Could not water plant: ", self.name)
			return False

	def check_water_level(self):
		self.arduino.write(b'3')
		response = self.arduino.readline()
		response = response.decode("ascii").rstrip('\r\n')
		if(response == "" or response == "1"):
			self.water_level = False
		elif(response == "0"):
			self.water_level = True

	def toggle_light(self):
		if(self.light_on): # Turn off light
			self.arduino.write(b'7')
			self.light_on = False
		else: # Turn on light
			self.arduino.write(b'6')
			self.light_on = True

		# Update neighbor plant (same arduino) status
		for plant in plants:
			if(plants[plant].arduino == self.arduino):
				plants[plant].light_on = self.light_on

	def get_info(self):
		# Send position (1 or 2) to request information for respective position
		self.arduino.write(self.position.encode(encoding="ascii"))

		# Read and decode response
		data = self.arduino.readline()
		data = data.decode("ascii")

		# If data received, update attributes and return True, else return False
		data = data.rstrip('\r\n').split(',')
		if(len(data) == 5):
			self.data_dict['temp'].append(int(data[0]))
			self.data_dict['humidity'].append(int(data[1]))
			self.data_dict['light'].append(int(data[2]))
			self.data_dict['soil_moisture'].append(int(data[3]))
			self.data_dict['soil_temp'].append(int(data[4]))
			return True

		return False

	# Function to average out existing data, empty data lists, and prepare a report
	# Returns a dictionary ready for posting as a log
	def get_report(self):
		self.check_water_level()

		data = {
			'plant_id': self.id,
			'timestamp': "",
			'water_level': self.water_level,
			'light_status': self.light_on
		}

		for key in self.data_dict:
			data[key] = round(sum(self.data_dict[key]) / len(self.data_dict[key]))
			self.data_dict[key].clear()
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
			' Tan\nHunter College, Spring 2020\n\n', sep ='')

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
	r = requests.get(HOST + "plants/all/" + email + "/")

	if(r.status_code != 200):
		print("Could not retrieve user configuration.")
		return False
	else:
		for entry in r.json():
			id = entry["plant_id"]
			if(id not in plants): # Add plant
				name = entry["plant_name"]
				port = entry["serial_port"]
				position = str(entry["position"])
				water_threshold = entry["water_threshold"]
				light_threshold = entry["light_threshold"]
				plants[id] = Plant(name, id, port, position, water_threshold,
					light_threshold)
				print("Added plant: " + name)
			else: # Update plant
				plants[id].name = entry["plant_name"]
				plants[id].water_threshold = entry["water_threshold"]
				plants[id].light_threshold = entry["light_threshold"]

	return True

# Function to cleanly exit the program
def cleanup():
	print("Stopping...")

	# Turn off lights and close all Serial connections
	for arduino in arduinos:
		arduinos[arduino].write(b'7')
		arduinos[arduino].close()

	print("Please reset and unplug your arduinos!")
	sys.exit()

def main():
	# Parse arguments:
	parser = argparse.ArgumentParser("Run a Synthesis garden.")
	parser.add_argument('--query_time', type=int, required=False, default=120,
		help="Specify in seconds the time elapsed between command queries.")
	parser.add_argument('--log_auto_time', type=int, required=False, default=3600,
		help="Specify in seconds the time elapsed between logging and checking\
			automated behavior")
	args = parser.parse_args()

	global run_program

	# Greet
	email, token = greet_and_login()

	# S3
	s3 = boto3.resource('s3')
	filename = "photos/" + email.split('@')[0] + ".png"

	# Set up listener for quit command
	listener = keyboard.Listener(on_press=on_press)
	listener.start()

	# Read in user configuration - loop while not successful
	while(not configure(email)):
		time.sleep(5)

	minute_tracker = time.time()
	log_auto_tracker = time.time()
	query_tracker = time.time()
	query_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

	# Primary Loop:
	while(run_program):
		# 1. Commands:
		# If greater than 120 seconds (2 minutes) - check for commands
		if(time.time() - query_tracker >= args.query_time):
			# For every plant...
			for plant in plants:
				curr_plant = plants[plant]
				# Check commands...
				r = requests.get(HOST + "requests/all/" + str(plant)
					+ "/" + query_time)

				if(r.status_code != 200):
					print("Could not retrieve requests for plant: ", curr_plant.name)
				else:
					# And process each command.
					# Only water once per batch of commands.
					watered = False
					for req in r.json():
						if(req['category'] == "water" and watered == False): # WATER
							curr_plant.water()
							# Email user if water() returns False

							watered = True
						elif(req['category'] == "light"): # LIGHT
							curr_plant.toggle_light()
						elif(req['category'] == "picture"): # PICTURE
							with PiCamera() as camera:
								stream = BytesIO()
								camera.capture(stream, format="png")
								stream.seek(0)
								s3.Bucket(BUCKET).put_object(Key=filename, Body=stream)

			query_tracker = time.time()
			query_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

		# 2. Data logging, configuration check and automated behavior:
		# If greater than 60 seconds - try twice to collect values for all plants 
		if(time.time() - minute_tracker >= 60):
			for plant in plants:
				curr_plant = plants[plant]
				if(not curr_plant.get_info()):
					if(not curr_plant.get_info()):
						print("Could not retrieve information for plant: ",
							curr_plant.name)

			minute_tracker = time.time()

		# If greater than 60 minutes:
		# 1) write log to database
		# 2) Water or turn on light as needed
		# 3) Check user configuration for plant additions or updates to
		#    plant names / thresholds
		if(time.time() - log_auto_tracker >= args.log_auto_time):
			for plant in plants:
				curr_plant = plants[plant]
				data = curr_plant.get_report()
				r = requests.post(HOST + "logs/insert", json=data)

				if(r.status_code != 200):
					print("Could not log data for plant: ", curr_plant.name)

				t = time.localtime()
				# Provide light between 9AM and 3PM (local time) if not
				# meeting threshold
				if((t.tm_hour >= 9 and t.tm_hour <= 15) and
					(not curr_plant.light_on) and
					(data['light'] < curr_plant.light_threshold)):
					curr_plant.toggle_light()

				# Turn off light thereafter
				if((t.tm_hour == 16 or t.tm_hour == 17) and
					(curr_plant.light_on)):
					curr_plant.toggle_light()

				# Check water level
				if((t.tm_hour == 7 or t.tm_hour == 8) and
					(not curr_plant.watered_today) and
					(data['soil_moisture'] < curr_plant.water_threshold)):
					curr_plant.water()
					# Email user if water() returns False
					curr_plant.watered_today = True

				# Reset watered flag
				if((t.tm_hour == 10 or t.tm_hour == 11) and
					(curr_plant.watered_today)):
					curr_plant.watered_today = False

			log_auto_tracker = time.time()

			configure(email)

		#time.sleep(10)

	cleanup()

if __name__ == '__main__':
	main()
