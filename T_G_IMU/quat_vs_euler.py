from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2 as IMU
from scipy.spatial.transform import Rotation as R
import time,  numpy as np
import threading

global queue
 
class Queue(object):
 
    def __init__(self):
        self.item = []
 
    def __str__(self):
        return "{}".format(self.item)
 
    def __repr__(self):
        return "{}".format(self.item)
 
    def enque(self, item):
        """
        Insert the elements in queue
        :param item: Any
        :return: Bool
        """
        self.item.insert(0, item)
        return True
 
    def size(self):
        """
        Return the size of queue
        :return: Int
        """
        return len(self.item)
 
    def dequeue(self):
        """
        Return the elements that came first
        :return: Any
        """
        if self.size() == 0:
            return None
        else:
            return self.item.pop()
 
    def peek(self):
        """
        Check the Last elements
        :return: Any
        """
        if self.size() == 0:
            return None
        else:
            return self.item[-1]
 
    def isEmpty(self):
        """
        Check is the queue is empty
        :return: bool
        """
        if self.size() == 0:
            return True
        else:
            return False


queue= Queue()

            
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

def acq():
    SUB_e, SUB_q = [], []
    n = 200
    for l in range(0,n):
        try:
            #quat
            w, x, y, z = imu.get_quaternion()
            w, x, y, z = w/16384, x/16384, y/16384, z/16384
            quat = [ x, y, z, w]
            r_q = R.from_quat(quat)
            m_q = r_q.magnitude()
            print(r_q.magnitude())
            
            #quat to deg
            rq_e = r_q.as_euler('xyz' , degrees=True)
            rq_e = R.from_euler('xyz', rq_e, degrees=True)
            m_qe = rq_e.magnitude()
            print(rq_e.magnitude())
            
            xe, ye, ze = imu.get_orientation()
            ze, xe, ye = ze/16, xe/16 , ye/16
            r_e = R.from_euler('xyz', [xe, ye, ze], degrees= True)
            m_e = r_e.magnitude()
            print(r_e.magnitude())
              
            #deg to quat
            re_q = r_e.as_quat()
            re_q = R.from_quat(re_q)
            m_eq = re_q.magnitude()
            print(m_eq)
            
        except ValueError:
            queue.enque([-1,-1])
            continue
        
        finally:
            sub_e = m_e - m_qe
            sub_q = m_q - m_eq
            SUB_e.append(sub_e)
            SUB_q.append(sub_q)
            time.sleep(0.1)
            l += 1
            
    queue.enque((SUB_e[1:], SUB_q[1:]))         

def mean(a):
    s = 0
    for i in range(0, len(a)):
        s += a[i]
    
    x_b = s/len(a)
    return x_b

def e_type(a):
    b = sorted(a)
    minimum = b[0]
    maximum = b[len(b)-1]
    e_type = maximum - minimum
    
    return e_type
        


'''
MAIN
'''
t = threading.Thread(target = acq)
t.start()
t.join()

sub_e, sub_q = queue.dequeue()

print(' Euler acq. & quat. to Euler | mean : {0} | std : {1}'.format(mean(sub_e),e_type(sub_e)))
print(' quat. acq. & Euler to quat. | mean : {0} | stdn: {1}'.format(mean(sub_q),e_type(sub_q)))
        
    


