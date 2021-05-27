import os
import numpy as np
import cv2
from datetime import datetime
import time
from picamera import PiCamera
import imutils

#Connection LED photomake sure that horizontal is multiple of 32 and vertical of 16
camera = PiCamera(resolution=(1024, 736))
camera.start_preview()
frq = 2 

#creation d'un objet pr stocker l'image
rawcapture = np.empty((1024 * 736 * 3,), dtype=np.uint8)

#Prise de la photo, et stockage en format PNG dans le dossier choisi : /home/pi/proto/Test/Image
i = 0
for frame in camera.capture_continuous(rawcapture, format  = 'bgr', use_video_port = True):
    img = frame.reshape(736 , 1024 , 3)
    img = imutils.rotate(img, 180)
    i += 1
    cv2.imwrite('/home/pi/proto/Camera_calibration/Image/Image_{0}.png'.format(i),img)
    
    time.sleep(1/frq)
    
    key = cv2.waitKey(1) & 0xFF
    if i >= 50:
        camera.stop_preview()   
            
cv2.destroyAllWindows()