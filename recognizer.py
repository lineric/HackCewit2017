import os
import cv2
import numpy
from PIL import Image

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

recognizer = cv2.createLBPHFaceRecognizer()

def get_photos(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.test.jpg')]
    print image_paths
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
            cv2.waitKey(200)
            
    return images, labels

path = './photos'
images, labels = get_photos(path)
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.waitKey(1)
cv2.waitKey(1)

recognizer.train(images, numpy.array(labels))

print "done training"

# Append the images with the extension .test.jpg into image_paths
image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.test.jpg')]
for image_path in image_paths:
    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = numpy.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    print faces
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        if nbr_actual == nbr_predicted:
            print "{} is Correctly Recognized with uncertainty {}".format(nbr_actual, conf)
        else:
            print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)
        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
        cv2.waitKey(1000)

cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.waitKey(1)
cv2.waitKey(1)
