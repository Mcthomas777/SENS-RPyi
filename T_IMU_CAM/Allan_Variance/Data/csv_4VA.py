import numpy as np
from picamera import PiCamera
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
from math import pi
import csv, sys, threading, cv2, time


def imu_acq(freq, imu, d):
        
    #csv header configuration
    Entete_csv = [
    'timestamp',
    'omega_x', 'omega_y', 'omega_z',
    'alpha_x' , 'alpha_y', 'alpha_z',
    ]
    
    path_csv = '/home/pi/Projet_Stage/Variance_Allan'
    csv_file = open( path_csv + '/imu_va.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(Entete_csv)
    
    t0 = time.time()
    t1 = 0
    while t1-t0 <= d  :  
        time.sleep(1.0/freq)
        xpp, ypp, zpp = imu.get_acceleration()
        thp, Php, Psp = imu.get_angular_velocity() 
        row = [
                    str(time.time_ns()), # temps en secondes depuis le début de l'expérience
                    str((thp/16)), str((Php/16)), str((Psp/16)), #en rad/s
                    str(xpp/100), str(ypp/100), str(zpp/100), #en m/s-2
                ]
        csv_writer.writerow(row)
        t1 = time.time()



"""
Definition of acquisition parameters (frequency of sampling, and duration) :
"""

freq_imu = 100 #Hz (imu)
d = 7200

#IMU connection

HOST = "localhost"
PORT = 4223
UID = "6yoKcp"

#connection to brick, and binding

ipcon = IPConnection()
imu = IMU(UID, ipcon)           
ipcon.connect(HOST, PORT) 

#few led blinking to announce that IMU is connecting

imu.leds_off()
for i in range(0,3):
    imu.leds_on()
    time.sleep(0.2)
    imu.leds_off()
    time.sleep(0.1)

#Check the fusion mode of data
"""
BrickIMUV2.SENSOR_FUSION_OFF = 0
BrickIMUV2.SENSOR_FUSION_ON = 1
BrickIMUV2.SENSOR_FUSION_ON_WITHOUT_MAGNETOMETER = 2
BrickIMUV2.SENSOR_FUSION_ON_WITHOUT_FAST_MAGNETOMETER_CALIBRATION = 3
"""
imu.set_sensor_fusion_mode(0)
a = imu.get_sensor_fusion_mode()

print('Fusion mode : ',a)
print('IMU data frequency : ' + str(freq_imu) + 'Hz')
print('time of experiment : ' + str(d/3600) + 'h')

"""
Main : recording gyrometrics and accelerations informations
"""
input("Click entr to begin recording...")

#Creating thread
th1 = threading.Thread(target= imu_acq,  args = (freq_imu, imu, d))

#starting thread
th1.start()
print("Logger started...")





