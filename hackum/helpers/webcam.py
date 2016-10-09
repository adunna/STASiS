import numpy as np
import cv2
import time
import base64
from clarifai_helper import *

cap = cv2.VideoCapture(-1)
runThrough = True

while(runThrough):
    frame = cap.read()[1]
    cnt = cv2.imencode('.png',frame)[1]
    print(clarifai_req(cnt))
    time.sleep(0.2)
    runThrough = False
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
