from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray

#initialize camera
camera = PiCamera()
camera.iso = 0
camera.framerate = 60
camera.resolution = [1920,1080]
raw = PiRGBArray(camera)

id = 1

sleep(0.1)
camera.capture('CheckerBoard_%d' % id, format = 'bgr')
sleep(2)
camera.capture('Checkerboard_raw_%d' % id, format = 'bgr')

print('Done %d') % id
