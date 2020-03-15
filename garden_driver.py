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
	def init(self):
		# DEFINE PORTS

		# DEFINE FLAGS
		# Errors
		self.error_water_tank = False
		self.error_light = False
		self.error_fan = False
		self.error_pump = False

		# Status
		self.pump_on = False
		self.light_on = False
		self.light_off = False

		# DATA

def main():
	# Define universal flags
	error_database = False
	request_data = False
	request_picture = False
	
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