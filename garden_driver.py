#! /usr/bin/env python3

# Authors: Daniel Mallia and Jayson Tan
# Date Begun: 3/14/2020

# This is the Python script intended to run on a Raspberry Pi and serve as
# the guiding "brain" of a synthesis garden's operation. It is called 
# garden_driver for this reason as well as because it acts as a software 
# driver, communicating with the actual hardware components.

import time
import serial

class Plant():
	def init(self, name, arduino, light, temp_humid, soil_temp, soil_moisture, 
			water_level, water_pump, fan, camera, light_thresh, temp_thresh,
			moisture_thresh):
		# DEFINE CHARACTERISTICS
		self.name = name
		self.arduino = arduino
		self.light = light
		self.temp_humid = temp_humid
		self.soil_temp = soil_temp
		self.soil_moisture = soil_moisture
		self.water_level = water_level
		self.water_pump = water_pump
		self.fan = fan
		self.camera = camera

		# DEFINE THRESHOLDS
        self.light_thresh = light_thresh
        self.temp_thresh = temp_thresh
        self.moisture_thresh = moisture_thresh

		# DEFINE FLAGS
		# Errors
		self.error_water_tank = False
		self.error_light = False
		self.error_fan = False
		self.error_pump = False

		# Status
		self.pump_on = False
		self.light_on = False
		self.fan_on = False


# Key Global Structures 
plants = {}		# Addresses Plant instances by name
hardware = {}	# Addresses Arduinos by name
				# Each Arduino it represented by a dictionary with a single 
				# connection : serial connection key-value pair
				# and multiple actuator : [on/off, error, **PlantNames] pairs

def main():
	# Define universal flags
	connection_error = False
	
	print("Serial library version: ", serial.__version__)

	# Primary Loop:
		# 1. Read the database control table
		# 		If error in read, set errorDatabase, and e-mail user
		# 		Else set command flags (Raspberry Pi)
		# 2. Process command flags
		# 		If dataNow - write average of existing saved values to table
		# 		If lightNow - turn on light
		# 		Etc. (Including checks that these were met - lightNow yields 
		# 			actual light on and such)
		# 3. Data logging:
		# 		If greater than 60 seconds - collect value (may want to poll 
		# 			now, get value on next loop)
		# 		If greater than 60 minutes - write average to database
		# 4. Process automated aspects:
		# 		Water if low moisture
		# 		Light if low light (and not night time)
		# 		etc.

if __name__ == '__main__':
    main()