# MAIN Pi LOOP
#name: frontpi
#login: pi
#password: abc

#Declarations
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
# initialize the camera and grab a reference to the raw camera capture
rawCapture = PiRGBArray(camera, size=(640, 480))

# OPENCV CONSTANTS
# colour ranges for the balls, BGR format: [lower],[upper]
# green yellow pink
boundaries = [([,,],[,,]),[,,],[,,]),([,,],[,,])]


# Poll for the Serial Request



# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array




# Run OpenCV Algo
# Prepare USB message

# clear the stream in preparation for the next frame
rawCapture.truncate(0)
# Return to loop
