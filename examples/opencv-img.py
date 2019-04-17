# OpenCV-Python: Getting started with images
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

import numpy as np
import cv2


img_path = 'img/dog.jpg'
img = cv2.imread(img_path)

bicycle = img[125:125+322, 101:101+486]
truck = img[81:81+87, 477:477+207]
dog = img[214:214+328, 134:134+179]

cv2.imshow('bicycle', bicycle)
cv2.imshow('truck', truck)
cv2.imshow('dog', dog)

cv2.waitKey(0)
cv2.destroyAllWindows()
