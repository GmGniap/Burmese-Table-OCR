import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./vision.json"

#from __future__ import print_function
from google.cloud import vision

image_uri = '../all/vision.png'

client = vision.ImageAnnotatorClient()
image = vision.Image()
image.source.image_uri = image_uri

response = client.text_detection(image=image)

for text in response.text_annotations:
    print('=' * 30)
    print(text.description)
    vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    print('bounds:', ",".join(vertices))
