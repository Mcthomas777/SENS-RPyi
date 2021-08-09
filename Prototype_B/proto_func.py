
import threading, os, time, datetime, csv
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge.bricklet_barometer_v2 import BrickletBarometerV2
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
from picamera import PiCamera
from fractions import Fraction
import numpy as np
import RPi.GPIO as GPIO
from astropy.io import fits
from astropy.io.fits import Header
                
def Take(iso, s_speed, imu, gps, path_img, rlb, t, b):
    
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
        img = camera.capture(path_img + "/img_{0}.data".format(i), 'rgb')
        GPS = get_GPS(gps, 1)#GPS = [date_gps, time_gps, lat, ns, long, ew,h, geoidal_separation] 
        lat = str(GPS[2]/1000000.0) + GPS[3] #DDdddd
        long = str(GPS[4]/1000000.0) + GPS[5] #DDdddd
        w,x,y,z = imu.get_quaternion()
        head,r,p = imu.get_orientation()
        T = get_T(t)
        P = get_P(b)
        quat = [x/16384,y/16384,z/16384,w/16384]
        euler = [head/16, r/16, p/16]
        imu.leds_off()
        
        #Converting into FITS
        width = 1472
        height = 1472
        fwidth = (width + 31) // 32 * 32
        fheight = (height + 15) // 16 * 16
        image = np.fromfile(path_img + "/img_{0}.data".format(i), dtype=np.uint8).reshape((fheight, fwidth, 3))
        R = image[:,:,0]
        G = image[:,:,1]
        B = image[:,:,2]
        #Not very robust way to reshape but it works pretty fine        
        p_fits = np.empty((3, fheight, fwidth))
        p_fits[0,:,:] = R
        p_fits[1,:,:] = G
        p_fits[2,:,:] = B
        
        hdr = Header({'SIMPLE': True, 'XTENSION' : 'IMAGE','BITPIX':8, 'NAXIS':3, 'NAXIS1':1472,
                      'NAXIS2': 1472, 'CTYPE3':'RGB','DATE':GPS[0], 'TIME':GPS[1], 'LAT':lat ,
                      'LONG':long, 'ALT':GPS[6]/100, 'q_x': quat[0], 'q_y':quat[1], 'q_z' : quat[2], 'q_w' : quat[3],
                      'head' : euler[0], 'roll' : euler[1], 'pitch' : euler[2], 'ISO' : iso, 'EXP. TIME' : s_speed,
                     'T' : T, 'P' : P})
        hdu = fits.PrimaryHDU(p_fits, header = hdr)
        hdul = fits.HDUList([hdu])
        hdr  = hdul[0].header
        print(repr(hdr))
        hdul.writeto(path_img+'/img_{0}.fits'.format(i), overwrite=True)
         
        state = rlb.get_button_state()
        i += 1
        if state == rlb.BUTTON_STATE_PRESSED:
            
            break
            
        
        
def darks(iso, s_speed, path_img):
    
    i = 0
    camera = PiCamera(resolution=(1472, 1472), framerate = Fraction(1, 2))
    camera.shutter_speed = s_speed
    camera.iso = iso
    time.sleep(30)
    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    
    while i<50 :
        img = np.empty((1472, 1472, 3), dtype=np.uint8)
        img = camera.capture(path_img + "/dark_{0}.data".format(i), 'rgb')
        i+=1
    
def data_a(imu, ipcon, path_dir, gps, rlb):
    #Definition de l'entete du fichier csv où seront stockés les données
    Entete_csv = [
    'Time gps', 
    'Lin. Acc. X [m.s-2]', 'Lin. Acc. Y [m.s-2]', 'Lin. Acc. Z [m.s-2]',
    'quat. w', 'quat. x', 'quat. y', 'quat. z',
    'head [°]', 'roll[°]', 'pitch[°]',
    'T [°C]', 'P [hPa]'
    ]

    csv_file = open(path_dir + '/logger.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(Entete_csv)
    rlb.set_color(124, 252, 30)
    try :
        while True :
            
            time.sleep(1.0/20)
            w,x,y,z = imu.get_quaternion()
            h,r,p = imu.get_orientation()
            xpp, ypp, zpp = imu.get_acceleration()
            date_gps, time_gps = get_GPS(gps, 0)
        
            row = [
                    str(time_gps), # temps en secondes depuis le début de l'expérience 
                    str(xpp/100), str(ypp/100), str(zpp/100),
                    str(w/16384), str(x/16384), str(y/16384), str(z/16384),
                    str(h/16), str(r/16), str(p/16)
                ]
            csv_writer.writerow(row)
          
            state = rlb.get_button_state()
            if state == rlb.BUTTON_STATE_PRESSED:
                rlb.set_color(255, 10, 10)               
                break
            
    except KeyboardInterrupt:
        pass
    
def get_GPS(gps, a):
    if a == 0:
        date_gps, time_gps = gps.get_date_time()
        return date_gps, time_gps
    elif a == 1:
        date_gps, time_gps = gps.get_date_time()
        lat, ns, long, ew = gps.get_coordinates()
        h, geoidal_separation  = gps.get_altitude()
        GPS = [date_gps, time_gps, lat, ns, long, ew,h, geoidal_separation] 
        return GPS
        
    

def get_T(t):
    '''
    return value of temperature in °C
    '''  
    T = t.get_temperature()
    T = T/100
    return T #output is originally in 1/100°C

def get_P(b):
    '''
    return value of pressure in hPa
    '''
    P = b.get_air_pressure()
    return P/1000 #output is originally in 1/1000 hPa

  


