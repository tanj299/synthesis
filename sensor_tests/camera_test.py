# Author:	Daniel Mallia
# Date:		4/19/2020
# Purpose:	This script contains a brief demonstration of the capabilities of
#			the Raspberry Pi Camera Rev. 1.3, using the picamera library.
#
#			This script draws upon the examples found at:
#			https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/4
#			https://picamera.readthedocs.io/en/release-1.13/recipes1.html			

import picamera
import time
#from io import bytesIO
#from PIL import Image

# Handles cleanup at end of block - avoiding explicit camera.close()
with picamera.PiCamera() as camera:
	# Set alpha (transparency) to allow viewing background
	# From documentation: "The camera module's preview system is quite crude:
	# it simply tells the GPU to overlay the preview on the Pi's video output."
	camera.start_preview(alpha=150)
	
	# Sleep to allow the sensor to detect lighting conditions
	time.sleep(2)
	
	img_name = "/home/pi/Desktop/" + time.strftime("%Y_%m_%d_%H_%M") + ".png"
	
	# Save locally
	camera.capture(img_name, resize=(640, 480))
	
	# Save in-memory for use with PIL - may need this 
	#stream = BytesIO()
	#camera.capture(stream, format=".png")
	#stream.seek(0)
	#image = Image.open(stream)

	time.sleep(10)
	camera.stop_preview()
