# Synthesis
## Statement
## Last Updated: 05/9/2020
### Synthesis - The Automatic Garden
### Authors: Leo Au-Yeung, Stanley Lim, Daniel Mallia, Jayson Tan
### Deployed website: http://synthesis-garden.herokuapp.com/ ###

This repository contains the code developed by the above authors in the 
Spring 2020 CSCI Capstone course under Professor Maryash at Hunter College, for 
the purpose of running an automated garden with a web interface. The hardware
heart of the project is a Raspberry Pi 3 Model B gathering data on, and 
tending to, a physical garden via an Arduino with numerous sensors, a light 
and a water pump.

Both `garden_driver.py`, the script for the Raspberry Pi, and `garden.ino`,
the sketch for the Arduino, were designed and written for use on a 
"prepackaged" product, where the user does not require much technical
expertise. The user need only be able to determine what USB port they plugged 
a given Arduino into on the Raspberry Pi.

Recreating this project is not difficult but requires adhering to a couple of 
requirements:
- The same hardware must be used: Raspberry Pi 3 Model B, Arduino Uno, and the sensors described in the sensor tests sketches. It would not be difficult to adapt the software to other similar hardware but we make no guarantees that the existing software will work with different hardware. Note: the specs for the light and water pump do not impact the software. For reference, we used a 12V LED light (~500 mA) and a 12V dosing pump (~300 mA) both controlled by the Arduino via Songle relays rated for 28V 10A DC output.
- A backend must be deployed. Refer to the README in the backend folder for more information.
- What will not be obvious from the existing software is that two external configuration files are required in order to run the picture functionality. There should be a hidden folder in the home directory, `~/.aws/`, containing two files: `config` and `credentials`. 

`config` should contain (adjusting for your server configuration): 
```
[default]
region=us-east-1
```

`credentials` should contain (substituting for your server credentials):
```
[default]
aws_access_key_id = YOUR ID
aws_secret_access_key = YOUR KEY
```

Please refer to the [boto3 Quick Start guide](https://pypi.org/project/boto3/) and the [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for more information.
