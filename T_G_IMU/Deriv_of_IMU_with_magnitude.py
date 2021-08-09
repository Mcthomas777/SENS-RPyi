from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
from scipy.spatial.transform import Rotation as R
import time,  numpy as np, csv
import matplotlib.pyplot as plt

def acquire_e(t):           
    #IMU connection
    HOST = "localhost"
    PORT = 4223
    UID = "6yoKcp"

    #connection to brick, and binding
    ipcon = IPConnection()
    imu = IMU(UID, ipcon)           
    ipcon.connect(HOST, PORT) 

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
    
        #Definition de l'entete du fichier csv où seront stockés les données
    Entete_csv = ['timestamp','xe', 'ye', 'ze']

    csv_file = open('/home/pi/Projet_Stage/Tgl_imu/imu0.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(Entete_csv)
    
    time.sleep(2)

    l, ts = [], [0]
    t0 = time.time()
    t1 = time.time()
    while t1-t0 < b:
        
        xe, ye, ze = imu.get_orientation()
        ze, xe, ye = ze/16, xe/16 , ye/16     
        l.append([xe, ye, ze])
        t1 = time.time()
        ts.append(t1-t0)
        print(t1-t0)
        
        row = [str(t1-t0),str(xe), str(ye), str(ze)]
        csv_writer.writerow(row)
        
    li = l[1:]

    r0 = R.from_euler('xyz', l[0], degrees = True)
    ri = R.from_euler('xyz', li, degrees= True)
    diff = (r0* ri.inv()).magnitude() 
    err = np.rad2deg(diff)*3600

    ts = ts[0:len(ts)-2]
    return err, ts

def acquire_f(b):           
    #IMU connection
    HOST = "localhost"
    PORT = 4223
    UID = "6yoKcp"

    #connection to brick, and binding
    ipcon = IPConnection()
    imu = IMU(UID, ipcon)           
    ipcon.connect(HOST, PORT) 

    #Check the fusion mode of data
    """
    BrickIMUV2.SENSOR_FUSION_OFF = 0
    BrickIMUV2.SENSOR_FUSION_ON = 1
    BrickIMUV2.SENSOR_FUSION_ON_WITHOUT_MAGNETOMETER = 2
    BrickIMUV2.SENSOR_FUSION_ON_WITHOUT_FAST_MAGNETOMETER_CALIBRATION = 3
    """
    imu.set_sensor_fusion_mode(1)
    a = imu.get_sensor_fusion_mode()
    print('Fusion mode : ',a)
    
        #Definition de l'entete du fichier csv où seront stockés les données
    Entete_csv = ['timestamp','xe', 'ye', 'ze']

    csv_file = open('/home/pi/Projet_Stage/Tgl_imu/imu0.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(Entete_csv)
    
    time.sleep(2)

    l, ts = [], [0]
    t0 = time.time()
    t1 = time.time()
    i=0
    while i < b:
        
        input('shake, then clck entr...')
        xe, ye, ze = imu.get_orientation()
        ze, xe, ye = ze/16, xe/16 , ye/16     
        l.append([xe, ye, ze])

        i +=1
        
    li = l[1:]

    r0 = R.from_euler('xyz', l[0], degrees = True)
    ri = R.from_euler('xyz', li, degrees= True)
    diff = (r0* ri.inv()).magnitude() 
    err = np.rad2deg(diff)*3600
    return err

def mean(a):
    s = 0
    for i in range(0, len(a)):
        s += a[i]
    
    x_b = s/len(a)
    return x_b


b = int(input("How many time (sec) : "))
err = acquire_f(b)
m_e = mean(err)
print(m_e)
plt.plot(err)
plt.title('Evolution of angle vs. time for a fixed position')
plt.xlabel('Time [s]')
plt.ylabel('Error [arcsec]')
plt.show()


# 
# s_x, s_y, s_z = 0
# for k in range(0,b):
#     s_x += d[k][0]
#     s_y += d[k][1]
#     s_z += d[k][2]
#     m_x = s_x/b
#     m_y = s_y/b
#     m_z = s_z/b
#     

# fig, ax = plt.subplot(223)
#  
# plt.subplot

        
        
    
            

