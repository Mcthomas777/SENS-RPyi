from tinkerforge.ip_connection import IPConnection, Error
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge.bricklet_barometer_v2 import BrickletBarometerV2
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton
from scipy.spatial.transform import Rotation as R
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
import numpy as np, math as m, os, csv
from astropy.io import fits
import threading, os, time, datetime, csv
import proto_func as f

HOST = "localhost"
PORT = 4223
ipcon = IPConnection() # Create IP connection

UID_lcd = 'R4w'
lcd = BrickletLCD128x64(UID_lcd, ipcon) # Create device object

UID_t = 'KN2'
t = BrickletTemperatureV2(UID_t, ipcon)

UID_b = 'NDR'
b = BrickletBarometerV2(UID_b, ipcon)

UID_btn = 'M2Y'
rlb = BrickletRGBLEDButton(UID_btn, ipcon)

UID_imu = "6yoKcp"
imu = IMU(UID_imu, ipcon)
  
UID_GPS = "PuL"
gps = BrickletGPSV2(UID_GPS, ipcon)

ipcon.connect(HOST, PORT)


def turning_on(lcd):
    lcd.clear_display()
    lcd.remove_all_gui()
    lcd.write_line(3, 5, "RPyi - SENS")
    time.sleep(2)
    

def config_choice(lcd):
    lcd.clear_display()
    lcd.remove_all_gui()
    
    lcd.write_line(0, 0, "ISO :")    
    lcd.write_line(4, 0, "exp. time [s]:")
    

    lcd.set_gui_slider(0, 54, 10, 68, lcd.DIRECTION_HORIZONTAL,30)
    lcd.set_gui_slider(1, 54, 45, 68, lcd.DIRECTION_HORIZONTAL, 30)
    lcd.set_gui_button(2, 5, 54, 20, 10, 'OK')

    
    lcd.set_gui_slider_value_callback_configuration(100, True)
    lcd.set_gui_slider_value_callback_configuration(100, True)
    
    state = False
    while state != True:
        state = lcd.get_gui_button_pressed(2)
        iso = lcd.get_gui_slider_value(0)
        s_speed = lcd.get_gui_slider_value(1)
        lcd.write_line(1, 0, "[{0}]".format(iso*10))
        lcd.write_line(5, 0, "[{0}] ".format(s_speed/10))
    time.sleep(0.5)
    return iso*10, s_speed*100000
        
def CSV(lcd):
    
    lcd.clear_display()
    lcd.remove_all_gui()
    
    lcd.write_line(0, 0, " Save inertial data")
    lcd.write_line(1, 0, " (Acc./Euler/Quat.) ")
    lcd.write_line(2, 0, " in.csv ?")    
    lcd.set_gui_button(0, 26, 32, 30, 15, 'YES')
    lcd.set_gui_button(1, 68, 32, 30, 15, 'NO')
    
    a = lcd.get_gui_button_pressed(0)
    b = lcd.get_gui_button_pressed(1)
    
    csv_st = bool()
    while a or b != True:
        a = lcd.get_gui_button_pressed(0)
        b = lcd.get_gui_button_pressed(1)
        
        if a == True:
            csv_st = True
        elif b == True:
            csv_st = False
  
    return csv_st
    
    
def Init_test(lcd):
    lcd.clear_display()
    lcd.remove_all_gui()
    lcd.write_line(3, 3, "Initializing...")
    time.sleep(2)
    
def boresight_axis_est(gps, imu, lcd):
    '''
    Combining position information (GPS), GPS time (UTC), orientation of camera, and harmonisation matrices
    We can figure out the attitude of the camera, i.e. the direction where the camera is pointing
    cam_IMU, and configuration of the scipy.Rotation are porper to our system, make sure it returns
    coherent informations with your camera attitude
    '''
    # CAM/UMI     X         Y           Z
    cam_IMU = [[0.1318, -0.9912, -0.01120],
               [-0.9908, -0.1321, 0.0285], 
               [-0.0297, 0.0073, -0.9995]]
    IMU_cam = np.transpose(cam_IMU)
    r_cam_IMU = R.from_matrix(cam_IMU)
    r_IMU_cam = R.from_matrix(IMU_cam)
    
            #Retourner caméra
    cam_camp = np.array([[1,0,0],
                         [0,-1,0],
                         [0,0,-1]])
    r_cam_azalt = R.from_matrix(cam_camp)
    
    lcd.clear_display()
    lcd.remove_all_gui()
    lcd.set_gui_button(2, 54, 54, 20, 10, 'OK')
    
    state = False
    while state != True:
        state = lcd.get_gui_button_pressed(2)

        # Def loc
        lat, ns, long, ew = gps.get_coordinates()
        lat = Angle(str(lat/1000000.0) + "°" +ns)
        long = Angle(str(long/1000000.0) + "°" +ew)
        h, geoidal_separation  = gps.get_altitude()
        loc = EarthLocation(lat=lat, lon=long, height=h*u.cm)

        # Def time
        date, time = gps.get_date_time()
        datetime = str(date) + " - " + str(time)
        t = Time.strptime(datetime, '%d%m%y - %H%M%S%f',scale='utc')

        # Quat
        w, x, y, z = imu.get_quaternion()
        r_imu_g_q = R.from_quat([x/16384, y/16384, z/16384, w/16384])

        #deg
        h, p,r = imu.get_orientation()
        euler_angles = [h/16, r/16, p/16]   
        r_imu_g_e = R.from_euler('xzy', euler_angles, degrees=True)

        # Az, Alt dela cam
        x_cam, y_cam, z_cam = (r_IMU_cam*r_imu_g_q*r_cam_azalt).as_euler('xzy', degrees = True)
        if z_cam < 0:
            z_cam = -z_cam-90
        elif z_cam > 0 :
            z_cam = z_cam-90

        #As euler angle are less accurate we basically choose quat
    #     x_came, y_came, z_came = (r_IMU_cam*r_imu_g_e).as_euler('zxy', degrees = True)
    #     print( x_came , y_came,  -z_came-90 )
      

        #local frame
        local_frame = AltAz(obstime=t,location=loc)
        az = Angle(x_cam*u.deg)#Angle(y_cam*u.deg)#.wrap_at()
        alt = Angle( (z_cam)*u.deg) #Angle(z_cam*u.deg)#.wrap_at()


        c_cam = SkyCoord(az, alt,  frame=local_frame)
        ra = c_cam.icrs.ra
        dec = c_cam.icrs.dec
        
        lcd.clear_display()
        lcd.remove_all_gui()
        lcd.set_gui_button(2, 54, 54, 20, 10, 'OK')
        lcd.write_line(1, 0, "Boresight Axis Estimation :")
        lcd.write_line(2, 3, "RA : {0}".format(ra))
        lcd.write_line(3, 3, "DEC : {0}".format(dec))
        lcd.write_line(4, 3, "Az CAM : {0}".format(az))
        lcd.write_line(5, 3, "Alt CAM : {0}".format(alt))
    

def reel_time_window(lcd,t,b, path, rlb):
    lcd.clear_display()
    lcd.remove_all_gui() 
    lcd.write_line(2, 1, "Test in process...")
    
    while True :
        lcd.clear_display()
        lcd.remove_all_gui()
        
        T = f.get_T(t)
        P = f.get_P(b)       
        nbr_element = len(os.listdir(path))
        if nbr_element%2 == 0:
            nbr_pics = nbr_element/2
        else :
            nbr_pics = (nbr_element-1)/2
        lcd.write_line(0, 1, "Test in process...")       
        lcd.write_line(2, 1, "Nbr. pics : {0}".format(nbr_pics))
        lcd.write_line(4, 1, "T [°C]: {0}".format(T))
        lcd.write_line(6, 1, "P [hPA] : {0}".format(P))
        state = rlb.get_button_state()
        if state == rlb.BUTTON_STATE_PRESSED:
            return False
        time.sleep(1)
        
def Dark_st(lcd):
    
        lcd.clear_display()
        lcd.remove_all_gui()
        
        lcd.write_line(1, 5, "End of test")
        lcd.write_line(3, 3, "Proceed to darks ?")
        
        lcd.set_gui_button(0, 26, 44, 30, 10, 'YES')
        lcd.set_gui_button(1, 68, 44, 30, 10, 'NO')
        
        a = lcd.get_gui_button_pressed(0)
        b = lcd.get_gui_button_pressed(1)
        
        drk_st = bool()
        while a != True or b != True :
            a = lcd.get_gui_button_pressed(0)
            b = lcd.get_gui_button_pressed(1)
            if a == True:
                drk_st = True
                break
            elif b == True:
                drk_st =  False
                break
        
        return drk_st
    
    
def Dark(lcd, iso, s_speed, datetime_gps, path_img):
        os.system('mkdir /home/pi/Desktop/Proto_b/Try_{0}/darks'.format(datetime_gps))
        os.system('sudo chmod 777 /home/pi/Desktop/Proto_b/Try_{0}/darks'.format(datetime_gps))
        path_img += '/darks'
        lcd.clear_display()
        lcd.remove_all_gui()
        lcd.write_line(4, 1, "50 Darks | Please wait...")
        f.darks(iso, s_speed, path_img)

def END_again(lcd):
    lcd.clear_display()
    lcd.remove_all_gui()
    
    lcd.write_line(1, 5, "Darks over")
    lcd.write_line(3, 3, "Another Try ?")
    
    lcd.set_gui_button(0, 26, 44, 30, 10, 'YES')
    lcd.set_gui_button(1, 68, 44, 30, 10, 'NO')
    
    a = lcd.get_gui_button_pressed(0)
    b = lcd.get_gui_button_pressed(1)
    again_st = bool()
    
    while a != True or b != True:
        a = lcd.get_gui_button_pressed(0)
        b = lcd.get_gui_button_pressed(1)
        print(a,b)
    
        if a == True:
            again_st = True
            break
        elif b == True:
            again_st = False
            break
            
    return again_st


'''
MAIN
'''
#Initialisation animation
for i in range(0,5):
    rlb.set_color(255, 182, 55)
    time.sleep(0.1)
    rlb.set_color(0, 0, 0)
    time.sleep(0.1)
                
turning_on(lcd)
again_st = True
while again_st == True:
    iso, s_speed = config_choice(lcd)
    print(iso, s_speed)
    csv_st = CSV(lcd)

    date_gps, time_gps = f.get_GPS(gps, 0)
    datetime_gps = str(date_gps) + '_' + str(time_gps)

    path_dir = '/home/pi/Desktop/Proto_b/Try_{0}'.format(datetime_gps)

    os.system('mkdir /home/pi/Desktop/Proto_b/Try_{0}'.format(datetime_gps))
    os.system('sudo chmod 777 /home/pi/Desktop/Proto_b/Try_{0}'.format(datetime_gps))


    th1 = threading.Thread(target = f.Take, args = [iso, s_speed, imu, gps, path_dir, rlb, t, b])
    th2 = threading.Thread(target = f.data_a, args = [imu, ipcon, path_dir, gps, rlb])
    th3 = threading.Thread(target = reel_time_window, args = [lcd,t,b, path_dir, rlb])

    boresight_axis_est(gps, imu, lcd)
    Init_test(lcd)

    if csv_st == True:
        th1.start()
        th2.start()
        th3.start()
    else:
        th1.start()
        th3.start()

    if csv_st == True:
        th1.join()
        th2.join()
        th3.join()
    else:
        th1.join()
        th3.join()


    drk_st = Dark_st(lcd)
    if drk_st == True:
        Dark(lcd, iso, s_speed, datetime_gps, path_img)
    elif drk_st == False:
        lcd.clear_display()
        lcd.remove_all_gui()
        lcd.write_line(3, 3, "No Darks")
        time.sleep(1)
           
    again_st = END_again(lcd)
    if again_st == True:
        agin_st = True
    elif again_st == False:
        lcd.clear_display()
        lcd.remove_all_gui()
        lcd.write_line(1, 3, "Thanks for using ")
        lcd.write_line(3, 3, "RPyi-SENS")
        lcd.write_line(5, 3, "BYE BYE")
        break
        


