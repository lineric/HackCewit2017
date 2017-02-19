import picamera
import RPi.GPIO as GPIO
import cv2
import sys
import os
import time
import picamera
import picamera.array
import numpy
import json
from PIL import Image
from socket import *

with open('stuff.json') as fp:
    data = json.load(fp)
cascPath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
GPIO.setmode(GPIO.BOARD)
stop = False
ping = False
camera = picamera.PiCamera()
camera.resolution = (208, 160)
camera.color_effects = (128,128)
camera.framerate = 32
rawCapture = picamera.array.PiRGBArray(camera, size=(208, 160))

recognizer = cv2.createLBPHFaceRecognizer()

def get_photos(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.test.jpg')]
    images = []
    labels = []
    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = numpy.array(image_pil, 'uint8')
        num = int(os.path.split(image_path)[1].split(".")[0].replace("subject",""))
        faces = faceCascade.detectMultiScale(image)
        for(x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(num)
            cv2.imshow("faces to training set", image[y: y + h, x: x + w])
            cv2.waitKey(10)
            
    return images, labels

path = './jsonstuff'
images, labels = get_photos(path)
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.waitKey(1)
cv2.waitKey(1)

recognizer.train(images, numpy.array(labels))

# PUD_UP because GND
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# One Example 
def capture(channel):
    global stop
    filename = 'test.jpg' #%(count)
    camera.capture(filename)
    stop = True

def my_exit(channel1):
    GPIO.cleanup()
    os._exit(0)

GPIO.add_event_detect(7, GPIO.FALLING, callback=capture)
GPIO.add_event_detect(11, GPIO.FALLING, callback=my_exit)

servername = '130.245.188.43'
serverport = 8061
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverport))
serverSocket.listen(1)

while True:
    print "server is listening"
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    print message
    if message == "KNOCKKNOCK":
        pinged = True
    time.sleep(1)
    while pinged:
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

            if stop == True:
                break

        cv2.destroyAllWindows()
        cv2.waitKey(1)
        cv2.waitKey(1)
        cv2.waitKey(1)

        time.sleep(2)
        
        if stop == True:
            predict_image_pil = Image.open("test.jpg").convert('L')
            predict_image = numpy.array(predict_image_pil, 'uint8')
            faces = faceCascade.detectMultiScale(predict_image)
            for (x, y, w, h) in faces:
                num_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
                sentence = "{} recognized with {} uncertainty".format(data[str(num_predicted)]["name"], conf)
                print sentence
                cv2.imshow("recognized", predict_image[y: y + h, x: x + w])
                cv2.waitKey(100)

            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            stop = False
            pinged = False
        connectionSocket.send(data[str(num_predicted)]["name"])
        connectionSocket.close()
                                
GPIO.cleanup() # clean up GPIO on normal exit 
