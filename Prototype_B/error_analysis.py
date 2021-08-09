from scipy.spatial.transform import Rotation as R
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
import numpy as np, math as m, os, csv
from astropy.io import fits


def astrometry(img, output_dir) :
    
    '''
    Function made to return WCS file, that countains RA/DEC, a.k.a attitude of the center of the image
    You can add a long list of options that are define in documentation (/T_CAM_ICRS/Astrometry)
    '''
    #we initilialize offline astrometry and take pictures in our directory
    AstroCommand = "solve-field"
    options = {'use-sextractor' : 1 ,
               'no-plot' : 0,
               'cpulimit 600' : 1, #time in s
               'D' : output_dir,
               'overwrite' : 0
               }
    
    args = [AstroCommand]
    
    for key, value in options.items():
        if value != 0 :
            ndashes = 1 if len(key) ==1 else 2
            args.append("{0}{1}".format(ndashes * '-', key))
            
    args.append(output_dir)
    args.append(img)
    
    cmd_bash = ''
    for i in range(0, len(args)):
        cmd_bash += str(args[i]) + ' '
        
    print(cmd_bash)
    os.system(cmd_bash)
    
def CAM_att(img, rfr_st):
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
    
    #Retourner caméra expression in Tgl
    cam_camp = np.array([[1,0,0],
                         [0,-1,0],
                         [0,0,-1]])
    r_cam_azalt = R.from_matrix(cam_camp)
    
    #getting information from image
    hdul = fits.open(img)
    hdr = hdul[0].header
    lat = hdr['LAT']
    long = hdr['LONG']
    h = hdr['ALT']
    date = str(hdr['DATE'])
    time = str(hdr['TIME'])
    datetime = date + ' - ' + time
    x = hdr['q_x']
    y = hdr['q_y']
    z = hdr['q_z']
    w = hdr['q_w']
    T = hdr['T']
    P = hdr['P']*100
    
    # Def loc
    loc = EarthLocation(lat=lat, lon=long, height=h*u.cm)
    # Def time
    t = Time.strptime(datetime, '%d%m%y - %H%M%S%f',scale='utc')
    # Quat
    r_imu_g_q = R.from_quat([x,y,z,w])
    # Az, Alt dela cam
    x_cam, z_cam, y_cam = (r_IMU_cam*r_imu_g_q*r_cam_azalt).as_euler('xzy', degrees = True)
    print( x_cam , z_cam,  y_cam )
    if y_cam < 0:
        y_cam = y_cam+90
    elif z_cam > 0 :
        y_cam = y_cam-90
#As euler angle are less accurate we basically choose quat
#     x_came, y_came, z_came = (r_IMU_cam*r_imu_g_e).as_euler('zxy', degrees = True)
#     print( x_came , y_came,  -z_came-90 )
    #local frame
    if rfr_st == True:
        local_frame_rfr = AltAz(obstime=t,location=loc, pressure= P*u.Pa, temperature=T*u.deg_C ,relative_humidity=0)
        local_frame = AltAz(obstime=t,location=loc)
        
        az = Angle(x_cam*u.deg)#Angle(y_cam*u.deg)#.wrap_at()
        alt = Angle((y_cam)*u.deg) #Angle(z_cam*u.deg)#.wrap_at()

        c_cam_rfr = SkyCoord(az, alt,  frame=local_frame_rfr)
        ra_rfr = c_cam_rfr.icrs.ra
        dec_rfr = c_cam_rfr.icrs.dec
        c_cam = SkyCoord(az, alt,  frame=local_frame)
        ra = c_cam.icrs.ra
        dec = c_cam.icrs.dec
        return ra_rfr, dec_rfr, ra, dec
    
    else:
        local_frame = AltAz(obstime=t,location=loc)
        
        az = Angle(x_cam*u.deg)#Angle(y_cam*u.deg)#.wrap_at()
        alt = Angle((y_cam)*u.deg) #Angle(z_cam*u.deg)#.wrap_at()

        c_cam = SkyCoord(az, alt,  frame=local_frame)
        ra = c_cam.icrs.ra
        dec = c_cam.icrs.dec
        return ra, dec
    
def CSV_att(wcs_path, wrtr, numb, img, RA_pred, DEC_pred):

    try: 
        wcs = fits.open(wcs_path)
        RA = wcs[0].header['CRVAL1']
        DEC = wcs[0].header['CRVAL2']        
    except :
        RA = 'none'
        DEC = 'none'
        pass
    
    row = [str(numb), str(RA), str(DEC), str(RA_pred), str(DEC_pred)]
    wrtr.writerow(row)
    return RA, DEC

def Stats(m, path, date, time, a, nbr_pics, b) :
    sucess_rate = (a/nbr_pics)*100
    
    if len(m) != 0 :
        RA_err = [m[i][2] for i in range(0, m.size)]
        DEC_err = [m[i][5] for i in range(0, m.size)]
        #Mean
        m_err_RA = np.mean(RA)
        m_err_DEC = np.mean(DEC)    
        #Min
        min_RA = np.amin(RA)
        min_DEC = np.amin(DEC)
        #Max
        max_RA = np.amax(RA)
        max_DEC = np.amax(DEC)
        #STD
        std_RA = np.std(RA)
        std_DEC = np.std(DEC)
    else :
        #Mean
        m_err_RA = 'none'
        m_err_DEC = 'none'    
        #Min
        min_RA = 'none'
        min_DEC = 'none'
        #Max
        max_RA = 'none'
        max_DEC = 'none'
        #STD
        std_RA = 'none'
        std_DEC = 'none'
        
    #écriture d'un fichier
    f = open(path+'/result.txt', 'w')
    f.write("Results test {0} - {1} UTC '\n'".format(date, time))
    if b == True :
        f.write("Correction Refraction ON'\n'")
    f.write("Sucess rate : {0}, [{1}/{2}]'\n'".format(sucess_rate,a,nbr_pics))
    f.write("Mean error[RA/DEC] : {0} | {1}'\n'".format(m_err_RA, m_err_DEC))
    f.write("Min/Max error[RA/DEC] : {0} | {1} / {2} | {3}'\n'".format(min_RA, min_DEC, max_RA, max_DEC))
    f.write("std [RA/DEC] : {0} | {1}'\n'".format(std_RA, std_DEC))
    f.close
    
def graph():
    '''
    still to developp
    problem : getting a stable reference value over the experiment to analyze properly the error 
    '''

'''MAIN'''
#Concerning file to study
# dir_n = 'essai_'+str(input('which session of test :'))
path = '/home/pi/Desktop/Proto_b' 
datetime = str(input('Which test do you want to study ? '))
try_n = '/Try_' + datetime
path = path+try_n

a = str(input('Would you study all pictures ? [y/n]'))
b = str(input('Would you consider atmosphere refraction ? [y/n]'))
c = str(input('Already pass through astrometry? [y/n]'))
if c == 'n' :
    d = str(input('Would you consider distortion? [y/n]'))
#TO DO : correction of distortion
    
    

nbr_element = len(os.listdir(path))
if nbr_element%2 == 0:
    nbr_pics = nbr_element/2
else :
    nbr_pics = (nbr_element-1)/2

print(nbr_pics)
#creating a csv file to stack attitude out of astrometry
#CSV header
Entete_csv = ["N","RA_pic","DEC_pic", "RA_pred", "DEC_pred"]
csv_file = open(path +'/attitude.csv', 'w')
wrtr = csv.writer(csv_file) #quoting=csv.QUOTE_ALL)
wrtr.writerow(Entete_csv)

#Creation of array to countain RA/DEC/err
Att_log = []

if a == 'y':
    
    #Processing all pictures from a one test
    for i in range(0,22):
        if c == 'n':
            '''astrometry'''
            img = path+'/img_{0}.fits'.format(i)
            output_dir = path+'/result_{0}'.format(i)
            astrometry(img, output_dir)
    
        '''dealing with astrometry data'''
        output_dir = path+'/result_{0}'.format(i)
        wcs_path = output_dir + '/img_{0}.wcs'.format(i)
        if b == 'y':
            RA_pred_rfr, DEC_pred_rfr, RA_pred, DEC_pred = CAM_att(img, True)
            RA, DEC = CSV_att(wcs_path, wrtr, i, img, RA_pred_rfr, DEC_pred_rfr)
        elif b == 'n':
            RA_pred, DEC_pred = CAM_att(img, False)
            RA, DEC = CSV_att(wcs_path, wrtr, i, img, RA_pred, DEC_pred)
        
        '''Position Logger creation'''
        a = 0
        if RA != 'none' or DEC != 'none':
            row = [RA, RA_pred, abs(RA_pred-RA), DEC, DEC_pred, abs(DEC_pred-DEC)]
            Att_log.append(row)
            a += 1 
        else :
            pass
        
    csv_file.close()
        
    '''DATA Analysis'''
    datetime = datetime.split('_')
    date = datetime[0]
    time = datetime[1]
    Stats(Att_log, path, date, time, a, nbr_pics, b)
    
    
else:
    pic_n = '/img_' + str(input('Which picture ? (Number 0-n)'))
    print('go on astrometry programm (/T_CAM_icrs/Astrometry)')