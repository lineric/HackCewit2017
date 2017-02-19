import cv2
import sys
import time
import picamera
import picamera.array
import numpy
from PIL import Image

cascPath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

camera = picamera.PiCamera()
camera.resolution = (300, 240)
camera.color_effects = (128,128)
camera.framerate = 32
rawCapture = picamera.array.PiRGBArray(camera, size=(300, 240))

# allow the camera to warmup
time.sleep(1)
 

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
