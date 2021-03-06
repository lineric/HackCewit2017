import picamera
import RPi.GPIO as GPIO
import os
import cv2
import sys
import time
import picamera.array
import numpy
from PIL import Image


cascPath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
camera = picamera.PiCamera()
GPIO.setmode(GPIO.BOARD)  
#camera.start_preview(fullscreen = False, window = (100,20,640,480))
count = 0
camera.resolution = (200, 150)
camera.color_effects = (128,128)
rawCapture = picamera.array.PiRGBArray(camera, size=(200, 150))

# PUD_UP because GND
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

time.sleep(1)

# One Example 
def capture(channel):
    global count
    filename = 'subject03.%d.jpg' %(count)
    camera.capture("./photos/" + filename)
    count += 1

def my_exit(channel1):
    os._exit(0)

GPIO.add_event_detect(7, GPIO.FALLING, callback=capture)
GPIO.add_event_detect(11, GPIO.FALLING, callback=my_exit)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img = frame.array

    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        #gray,
        img,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF
 
    rawCapture.truncate(0)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.waitKey(1)
cv2.waitKey(1)

  
GPIO.cleanup() # clean up GPIO on normal exit 
