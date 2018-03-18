from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray

#initialize camera
camera = PiCamera()
camera.iso = 0
camera.framerate = 60
camera.resolution = [640,480]

# capture parameters
time = 30
Hz = 1
delay = 1/float(Hz)

id = 0
while id < (time*Hz):
 filename = "image_%d" % (id)
 camera.capture(filename, 'bgr')
 sleep(delay)
 id += 1
