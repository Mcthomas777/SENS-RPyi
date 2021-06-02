import time, os, cv2
from picamera import PiCamera
import matplotlib.pyplot as plt
import matplotlib.image as plm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from fractions import Fraction
import numpy as np


"""  
camera.brightness = 50 (0 to 100)
camera.sharpness = 0 (-100 to 100)
camera.contrast = 0 (-100 to 100)
camera.saturation = 0 (-100 to 100)
camera.iso = 0 (automatic) (100 to 800)
camera.exposure_compensation = 0 (-25 to 25)
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

For more information check : https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
""" 

def pics():
    
    a = input('Press entr to begin...')


    for i in range (100,601,100):
        os.system('mkdir image_set/iso_{0}'.format(i))
        
        for j in range (500000,10000001,500000):
            
            camera = PiCamera(resolution=(2048, 1472), framerate=Fraction(1, 10)) #max exposure time = 1/min framerate (for 10s, framerate 1/10)
            camera.iso = i
            camera.shutter_speed = j
            
            # Give the camera a good long time to set gains and
            # measure AWB (you may wish to use fixed AWB instead)
            time.sleep(5)
            camera.exposure_mode = 'off'
            
            t0 = time.time()
            img = camera.capture("image_set/iso_{0}/image_s-{1}.png".format(i,j/1000000))
            print(time.time()-t0)
            camera.close()


def histogram(iso, sspeed):
        
    path = "image_set/iso_" + str(iso) + "/image_s-" + str(sspeed) + ".png"
    img = cv2.imread(path)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    row, cols, d = img.shape
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    v_pix_r = [0]*256
    v_pix_g = [0]*256
    v_pix_b = [0]*256
    v_pix = [0]*256
    for i in range(0, row, 1):
        for j in range(0, cols, 1):
            v_pix_r[r[i,j]] += 1
            v_pix_g[g[i,j]] += 1
            v_pix_b[b[i,j]] += 1
            v_pix[grey[i,j]] += 1
            
    plt.subplot(2,1,1)
    plt.plot(v_pix_r, label = 'Red', color ='r')
    plt.plot(v_pix_g, label = 'Green', color = 'g')
    plt.plot(v_pix_b,label = 'Blue', color = 'b')
    plt.title('Repartition of pixel in the three layer')
    plt.legend()
    
    plt.subplot(2,1,2)
    plt.plot(v_pix)
    plt.title('Repartitin of pixel on grayscale')
    
    plt.show()

def plot_pics(iso):
    path = "image_set/iso_" + str(iso)
    os.system('cd ' + path)
    
    ssp = 0.5
    k = 1
    
    for i in range(0, 5):
        for j in range(0, 4):
            
            #Plot configuration
            plt.subplot(5,4,k)
            plt.title(str(ssp)+'sec')
            plt.axis('off')
            
            #Displaying pictures
            pics = plm.imread(path +'/image_s-'+ str(ssp) +'.png')
            im = plt.imshow(pics)
             
            
            ssp += 0.5
            k += 1
            
         
    plt.show()   



"""
=================================
MAIN
=================================
"""

a = int(input("""Press any of following key for any options
                Options : create data set --> 1
                          histogram of a picture --> 2
                          plot iso vs. sspeed --> 3 :
                          exit --> 4
                          """))
if a == 1 :
    pics()
    
if a == 2 :
    print(' From which pictures would you like to have the histogram')
    iso = int(input("enter iso parameter (100-800) : "))
    sspeed = float(input("enter shutter speed parameter (0.5 to 10) : "))
    histogram(iso, sspeed)

if a == 3 :
    print(' From which dataset would you like the plot')
    iso = int(input("enter iso parameter (100-800) : "))
    plot_pics(iso)
    
if a== 4 :
    print('have a nice day')
    


