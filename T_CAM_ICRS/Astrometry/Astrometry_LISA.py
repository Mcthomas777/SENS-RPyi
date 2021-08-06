import os
from astrometry.util.util import Sip
import subprocess
import tempfile


def astrometry(img, output_dir ) :
    #we initilialize offline astrometry and take pictures in our directory
    AstroCommand = "solve-field"
    options = {'use-sextractor' : 1 ,
               'no-plot' : 0,
               'cpulimit 600' : 1, #time in s
               'D' : output_dir,
               }
    
    args = [AstroCommand]
    #regarding chosen options, following loop is filling with these activated 
    for key, value in options.items():
        if value != 0 :
            ndashes = 1 if len(key) ==1 else 2
            args.append("{0}{1}".format(ndashes * '-', key))
            
    args.append(output_dir)
    args.append(img)
    
    #compiling list into a list of charachter
    cmd_bash = ''
    for i in range(0, len(args)):
        cmd_bash += str(args[i]) + ' '
        
    print(cmd_bash)

    os.system(cmd_bash)

output_dir = '/home/pi/Projet_Stage/Astro'
img = '/home/pi/Projet_Stage/Astro/img_5.fits'
astrometry(img, output_dir)
