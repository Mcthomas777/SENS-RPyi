import os
import numpy as np
import cv2
from datetime import datetime
import time
from picamera import PiCamera

#matrice des paramètres intrinsèques 
mtx = np.array([[840.74050124,   0,         507.10681845],
 [  0,         837.99969241, 357.10242472],
 [  0,           0,          1        ]])
    
#matrice de distorsion
dist = np.array([ 0.25556647 ,-0.53294573 , 0.00254167 ,-0.00189429 , 0.31808413])  


img = cv2.imread("/home/pi/proto/Camera_calibration/Image/Image_8.png")
h, w = img.shape[:2]
newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
undst = cv2.undistort(img, mtx, dist, None, newCameraMtx)
    
cv2.imwrite('/home/pi/proto/Camera_calibration/Image/Image_8_undst.png',undst)
