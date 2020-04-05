
import io
import os
from datetime import datetime

import cv2
from google.cloud import vision_v1p3beta1 as vision

# Setup google authen client key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'

# Source path content all images
SOURCE_PATH = "C:/Users/vmironov/Fruit/"
OUTPUT_PATH = "C:/Users/vmironov/Fruit_res3/"

FOOD_TYPE = 'Fruit'


def recognize_food(img_path):

    # Read image with opencv
    img = cv2.imread(img_path)

    # Get image size
    height, width = img.shape[:2]

    # Scale image
    img = cv2.resize(img, (800, int((height * 800) / width)))
    #Image cutting
    # height, width = img.shape[:2]
    # height = int(height/2)
    # width = int(width/2)
    # img = img[0:2*height, 0:width]

    # Save the image to temp file
    cv2.imwrite(SOURCE_PATH + "output.jpg", img)

    # Create new img path for google vision
    img_path = SOURCE_PATH + "output.jpg"

    # Create google vision client
    client = vision.ImageAnnotatorClient()

    # Read image file
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    #Segmentation
    objects = client.object_localization(image=image).localized_object_annotations
    # print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        # print('\n{} (confidence: {})'.format(object_.name, object_.score))
        # print('Normalized bounding polygon vertices: ')
        # print(object_.bounding_poly.normalized_vertices)

        #writing rectangle
        height, width = img.shape[:2]
        a = int(800*object_.bounding_poly.normalized_vertices[0].x)
        b = int(height*object_.bounding_poly.normalized_vertices[0].y)
        c = int(800*object_.bounding_poly.normalized_vertices[2].x)
        d = int(height*object_.bounding_poly.normalized_vertices[2].y)
        cv2.rectangle(img,(a,b),(c,d),(50,50,200),2)

        #first option to recognize
        cv2.putText(img,object_.name,(int((a+c)/2),int((b+d)/2)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)

        #second option to recognize (NOT PRODUCTIVE IN TIME)
        # segment = img[b:d,a:c]
        # cv2.imwrite(SOURCE_PATH + "peace.jpg", segment)
        # img_path = SOURCE_PATH + "peace.jpg"
        # client = vision.ImageAnnotatorClient()
        # with io.open(img_path, 'rb') as image_file:
        #     content = image_file.read()
        # segment = vision.types.Image(content=content)
        # objects_new = client.object_localization(image=image).localized_object_annotations
        # for object in objects_new:
        #     desc = object_.name
        # cv2.putText(img, desc, (a, int((b + d) / 2)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 255), 2)

        #third option to recognize(NOT PRODUCTIVE IN TIME, DOESNT CORRECTLY WORKS)
        # segment = img[b:d, a:c]
        # cv2.imwrite(SOURCE_PATH + "peace.jpg", segment)
        # img_path = SOURCE_PATH + "peace.jpg"
        # client = vision.ImageAnnotatorClient()
        # with io.open(img_path, 'rb') as image_file:
        #     content = image_file.read()
        # segment = vision.types.Image(content=content)
        # response = client.label_detection(image=segment)
        # labels = response.label_annotations
        # for label in labels:
        #     desc = label.description.lower()
        #     break
        # cv2.putText(img, desc, (a, int((b + d) / 2)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 255),2)

    cv2.imshow('Recognize & Draw', img)
    cv2.waitKey(0)
    return img


print('---------- Start FOOD Recognition --------')
start_time = datetime.now()
for k in range(4,5):
    path = SOURCE_PATH + '{id}.jpg'.format(id=k)
    res = recognize_food(path)
    cv2.imwrite(OUTPUT_PATH + "{id}.jpg".format(id=k), res)
print('Total time: {}'.format(datetime.now() - start_time))
print('---------- End ----------')