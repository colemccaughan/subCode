import numpy as np
#import serial
import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

#red 0-8, yellow 13-30, green 37-50
yellow_lower = np.array([25,160,100], np.uint8)
yellow_upper = np.array([35,255,255], np.uint8)
pink_lower = np.array([165,150,90], np.uint8)
pink_upper = np.array([180,255,255], np.uint8)
green_lower = np.array([45,150,90], np.uint8)
green_upper = np.array([60,255,255], np.uint8)

bounds = [(pink_lower,pink_upper), (yellow_lower, yellow_upper), (green_lower, green_upper)]

#import image
#image = cv2.imread("TestImage.jpg")

#camera setup
camera = PiCamera()
camera.framerate = 24
camera.iso = 0
camera.resolution = [640,480]
raw = PiRGBArray(camera, size=[640,480])
#wait for serial

#capture image
camera.capture(raw, format="bgr", use_video_port=True)
image = raw.array
#image = raw.reshape((1080,1920,3))

#Preprocess
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

#cv2.imshow("HSV", hsv)
#cv2.imshow("Blurred", blurred)

#generate masks for each colour
pink_mask = cv2.inRange(blurred, pink_lower, pink_upper)
pink_mask = cv2.erode(pink_mask, None, iterations=1)
pink_mask = cv2.dilate(pink_mask, None, iterations=1)
yellow_mask = cv2.inRange(blurred, yellow_lower, yellow_upper)
yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
yellow_mask = cv2.dilate(yellow_mask, None, iterations=1)
green_mask = cv2.inRange(blurred, green_lower, green_upper)
green_mask = cv2.erode(green_mask, None, iterations=1)
green_mask = cv2.dilate(green_mask, None, iterations=1)

mask_array = [pink_mask,yellow_mask,green_mask]

cv2.imshow("Pink", pink_mask)
cv2.imshow("Yellow", yellow_mask)
cv2.imshow("Green", green_mask)

id = 0
found_balls = []

while id < 3:
 #find contours
 cnt = cv2.findContours(mask_array[id].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
 center = None

 for i in range(len(cnt)):
  area = cv2.contourArea(cnt[i])
  if area > 400:
   (x,y), radius = cv2.minEnclosingCircle(cnt[i])
   calc_area = int(radius)*int(radius)*3.14
  # if float(area)/calc_area > 0.6:
   center = (int(x),int(y))
   radius = int(radius)
   found_balls.append([x,y,radius,id])
   cv2.circle(image,center,radius,(0,0,255),2)
 id += 1

print(found_balls)
cv2.imshow("Image", image)
cv2.waitKey(0)
