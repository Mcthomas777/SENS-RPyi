from scipy.spatial.transform import Rotation as R
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2 
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
import numpy as np, math as m


HOST = "localhost"
PORT = 4223
UID_IMU = "6yoKcp"
UID_GPS = "PuL"

ipcon = IPConnection()
ipcon.connect(HOST, PORT)
# Création de l'objet imu
imu = IMU(UID_IMU, ipcon)            
# Création de l'objet imu 
gps = BrickletGPSV2(UID_GPS, ipcon)

# CAM/UMI     X         Y           Z
cam_IMU = [[0.1318, -0.9912, -0.01120],
           [-0.9908, -0.1321, 0.0285], 
           [-0.0297, 0.0073, -0.9995]]
IMU_cam = np.transpose(cam_IMU)
r_cam_IMU = R.from_matrix(cam_IMU)
r_IMU_cam = R.from_matrix(IMU_cam)


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
r_imu_g = R.from_quat([x/16384, y/16384, z/16384, w/16384])

#Retourner caméra
cam_camp = np.array([[1,0,0],
                     [0,-1,0],
                     [0,0,-1]])
r_cam_azalt = R.from_matrix(cam_camp)

# Az, Alt dela cam
x_cam, y_cam, z_cam = (r_IMU_cam*r_imu_g*r_cam_azalt).as_euler('zxy', degrees = True)
print( x_cam , y_cam,  -z_cam-90 )

#local frame
local_frame = AltAz(obstime=t,location=loc)
az = Angle(y_cam*u.deg)#Angle(y_cam*u.deg)#.wrap_at()
alt = Angle( (-z_cam-90)*u.deg) #Angle(z_cam*u.deg)#.wrap_at()
print(alt, az)

c_cam = SkyCoord(az, alt,  frame=local_frame)
print(c_cam.icrs)
# # 
# 
# 
# 
# 
# 