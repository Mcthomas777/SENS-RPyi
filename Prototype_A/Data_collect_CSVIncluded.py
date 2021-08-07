
import threading, os, time, datetime, csv
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
from picamera import PiCamera
from fractions import Fraction
import numpy as np
import RPi.GPIO as GPIO
from astropy.io import fits
from astropy.io.fits import Header

#Configuration
"""
GPIO numbering mode
=============================
GPIO.BCM --> GPIO numbering
GPIO.BOARD -->  pin numbering
"""
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN)
GPIO.setup(16, GPIO.IN)

               
def Take(iso, s_speed, imu, date, gps):
    
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
    """ 
    
    #connection LED photo
    imu.leds_off()
    
    i = 0
    camera = PiCamera(resolution=(1472, 1472), framerate = Fraction(1, 2))
    camera.shutter_speed = s_speed
    camera.iso = iso
    time.sleep(30)
    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    imu.leds_off()
    
    while True :
        #Capturing pictures, LEDS can be remove, just to let us know that program is running, when not using screen
        imu.leds_on()
        img = np.empty((1472, 1472, 3), dtype=np.uint8)
        img = camera.capture("/home/pi/Projet_Stage/Prototype_A/ST/Try_{1}/img_{0}.data".format(i, date), 'rgb')
        date_gps, time_gps = gps.get_date_time()
        lat, ns, long, ew = gps.get_coordinates()
        lat = str(lat/1000000.0) +ns #DDdddd
        long = str(long/1000000.0) +ew #DDdddd
        h, geoidal_separation  = gps.get_altitude()
        w,x,y,z = imu.get_quaternion()
        h,r,p = imu.get_orientation()
        quat = [x/16384,y/16384,z/16384,w/16384]
        euler = [h/16, r/16, p/16]
        imu.leds_off()
        
        #Converting into FITS
        width = 1472
        height = 1472
        fwidth = (width + 31) // 32 * 32
        fheight = (height + 15) // 16 * 16
        image = np.fromfile("/home/pi/Projet_Stage/Prototype_A/ST/Try_{1}/img_{0}.data".format(i, date), dtype=np.uint8).reshape((fheight, fwidth, 3))
        R = image[:,:,0]
        G = image[:,:,1]
        B = image[:,:,2]
        #Not very robust way to reshape but it works pretty fine        
        p_fits = np.empty((3, fheight, fwidth))
        p_fits[0,:,:] = R
        p_fits[1,:,:] = G
        p_fits[2,:,:] = B
        
        hdr = Header({'SIMPLE': True, 'XTENSION' : 'IMAGE','BITPIX':8, 'NAXIS':3, 'NAXIS1':1472,
                      'NAXIS2': 1472, 'CTYPE3':'RGB','DATE':date_gps, 'TIME':time_gps, 'LAT':lat ,
                      'LONG':long, 'ALT':h/100, 'q_x': quat[0], 'q_y':quat[1], 'q_z' : quat[2], 'q_w' : quat[3],
                      'head' : euler[0], 'roll' : euler[1], 'pitch' : euler[2], 'ISO' : iso, 'EXP. TIME' : s_speed})
        hdu = fits.PrimaryHDU(p_fits, header = hdr)
        hdul = fits.HDUList([hdu])
        hdr  = hdul[0].header
        print(repr(hdr))
        hdul.writeto('/home/pi/Projet_Stage/Prototype_A/ST/Try_{1}/img_{0}.fits'.format(i, date), overwrite=True)
        
        i += 1
        if GPIO.input(26) == True :
            camera.close()
            os.system('pkill $(pgrep -f /home/pi/Projet_Stage/Prototype_A/ST/Data_collect_CSVIncluded.py)')
            break
    
def data_a(imu, ipcon, frq, date, gps):
    #Definition de l'entete du fichier csv où seront stockés les données
    Entete_csv = [
    'Time gps', 
    'Lin. Acc. X', 'Lin. Acc. Y', 'Lin. Acc. Z',
    'head', 'roll', 'pitch'
    ]

    csv_file = open('/home/pi/Projet_Stage/Prototype_A/ST/Try_{1}/log_{0}.csv'.format(frq, date), 'w')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(Entete_csv)

    try :
        while True :
            
            time.sleep(1.0/frq)
            w,x,y,z = imu.get_quaternion()
            h,r,p = imu.get_orientation()
            xpp, ypp, zpp = imu.get_acceleration()
            date_gps, time_gps = gps.get_date_time()
        
            row = [
                    str(time_gps), # temps en secondes depuis le début de l'expérience 
                    str(xpp/100), str(ypp/100), str(zpp/100),
                    str(w/16384), str(x/16384), str(y/16384), str(z/16384),
                    str(h/16), str(r/16), str(p/16)
                ]
            csv_writer.writerow(row)
            
            if GPIO.input(26) == True :
                ipcon.disconnect()
                os.system('pkill $(pgrep -f /home/pi/Projet_Stage/Prototype_A/ST/Data_collect_CSVIncluded.py)') 
                break
        
    except KeyboardInterrupt:
        pass

"""
MAIN
"""
if GPIO.input(16) == False:
    iso = 600
    s_speed = 800000 #ms

if GPIO.input(16) == True:
    iso = 200
    s_speed = 2000000 #ms    

'''
We can add a third switch or state LED
# GPIO.setup(5, GPIO.IN)
# if GPIO.input(5) == False:
'''
freq = 100#Hz (IMU acquisition frequency)

#Definition variable conncetion periph.
HOST = "localhost"
PORT = 4223
UID = "6yoKcp"
UID_GPS = "PuL"

#Binding des periph.
ipcon = IPConnection() 
ipcon.connect(HOST, PORT) 

#creation des objets IMU/GPS
imu = IMU(UID, ipcon) 
gps = BrickletGPSV2(UID_GPS, ipcon)

#Routine purement esthétique pour indiquer le démarage
imu.leds_off()
for i in range(0,3):
    imu.leds_on()
    time.sleep(0.2)
    imu.leds_off()
    time.sleep(0.1)

#extinction des lumières de l'IMU
imu.leds_off()

#définition de la date 
date, time_gps = gps.get_date_time()
date = str(date) + '_' + str(time_gps)
os.system('mkdir /home/pi/Projet_Stage/Prototype_A/ST/Try_{0}'.format(date))
os.system('sudo chmod 777 /home/pi/Projet_Stage/Prototype_A/ST')
                
th1 = threading.Thread(target = Take, args = [iso, s_speed, imu, date, gps])
th2 = threading.Thread(target = data_a, args = [imu, ipcon, freq, date, gps])

th1.start()
th2.start()

  


