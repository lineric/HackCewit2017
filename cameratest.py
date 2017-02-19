import picamera
import RPi.GPIO as GPIO
import os

camera = picamera.PiCamera()
GPIO.setmode(GPIO.BOARD)  
camera.start_preview(fullscreen = False, window = (100,20,640,480))
count = 0
camera.resolution = (300, 240)
camera.color_effects = (128,128)

# PUD_UP because GND
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# One Example 
def capture(channel):
    global count
    filename = 'testerStan.jpg'# %(count)
    camera.capture(filename)
    count += 1

def my_exit(channel1):
    os._exit(0)

GPIO.add_event_detect(7, GPIO.FALLING, callback=capture)
GPIO.add_event_detect(11, GPIO.FALLING, callback=my_exit)

while True: # Loop forever
  True
  
GPIO.cleanup() # clean up GPIO on normal exit 
