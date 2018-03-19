import numpy as np
import time
import cv2
#from picamera import PiCamera
#from picamera.array import PiRGBArray

#red 0-8, yellow 13-30, green 37-50
yellow_lower = np.array([20,160,100], np.uint8)
yellow_upper = np.array([35,255,255], np.uint8)
pink_lower = np.array([0,150,90], np.uint8)
pink_upper = np.array([10,255,255], np.uint8)
green_lower = np.array([38,100,90], np.uint8)
green_upper = np.array([50,255,255], np.uint8)

bounds = [(pink_lower,pink_upper), (yellow_lower, yellow_upper), (green_lower, green_upper)]

image = cv2.imread('UnderwaterBalls.jpg')
image = cv2.resize(image, (640,480))

#camera setup
#camera = PiCamera()
#camera.framerate = 60
#camera.iso = 0
#camera.resolution = (640,480)
#raw = PiRGBArray(camera, size=(640,480))

st = time.time()

#capture image
#camera.capture(raw, format='bgr', use_video_port=True)
#image = raw.array

#Preprocess
blurred = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
cvt = time.time()

#repetitions
rep = 1
#generate masks for each colour
pink_mask = cv2.inRange(blurred, pink_lower, pink_upper)
pink_mask = cv2.erode(pink_mask, None, iterations=rep)
#pink_mask = cv2.dilate(pink_mask, None, iterations=rep)

yellow_mask = cv2.inRange(blurred, yellow_lower, yellow_upper)
yellow_mask = cv2.erode(yellow_mask, None, iterations=rep)
#yellow_mask = cv2.dilate(yellow_mask, None, iterations=rep)

green_mask = cv2.inRange(blurred, green_lower, green_upper)
green_mask = cv2.erode(green_mask, None, iterations=rep)
#green_mask = cv2.dilate(green_mask, None, iterations=rep)

mask_array = [pink_mask,yellow_mask,green_mask]

enmask = time.time()

#cv2.imshow("HSV", hsv)
#cv2.imshow("Blurred", blurred)
#cv2.imshow("Pink", pink_mask)
#cv2.imshow("Yellow", yellow_mask)
#cv2.imshow("Green", green_mask)

found_balls = []

stwhile = time.time()

for id in range(0,3):
#find contours
 cnt = cv2.findContours(mask_array[id].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
 center = None
 for i in range(len(cnt)):
  area = cv2.contourArea(cnt[i])
  if area > 100:
   (x,y), radius = cv2.minEnclosingCircle(cnt[i])
   center = (int(x),int(y))
   radius = int(radius)
   found_balls.append([center,radius,id])
   cv2.circle(image,center,radius,(0,0,255),2)

en = time.time()
print(found_balls)
print('st %.3f') % st
print('cvt %.3f') % cvt
print('enmask %.3f') % enmask
print('stwhile %.3f') % stwhile
print('end %.3f') % en
print('total %.3f') % (en-st)
print(len(cnt))

cv2.imshow("Image", image)
cv2.waitKey(0)
