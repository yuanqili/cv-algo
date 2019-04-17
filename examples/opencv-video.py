# OpenCV-Python: Getting started with videos
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import cv2


video = cv2.VideoCapture('video/webcam-ivanec.mp4')

while True:
    # Captures frame-by-frame
    ret, frame = video.read()
    if not ret:
        break
    # Processes the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Displays the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
