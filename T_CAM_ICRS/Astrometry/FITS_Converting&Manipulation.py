import numpy as np
from astropy.io import fits

#Manipulation of FITS_file
#In this example we have a Fits file with just a picture and a header
#opening fits file
stream = "/home/pi/Projet_Stage/Astro/img_10.fits"
hdulist = fits.open(stream)
#Getting info about files as number of element, and data type...
hdulist.info()
#First you have a header that you can extract quite easily
hdr  = hdulist[0].header
print(repr(hdr))
#And there is the picture
image = hdulist['PRIMARY'].data


#Converting into FITS
width = 1472
height = 1472
fwidth = (width + 31) // 32 * 32
fheight = (height + 15) // 16 * 16

#opening the our data type image, which appear like a 1D array, and that we reshape into a more casual standard
image = np.fromfile("/home/pi/Projet_Stage/Astro/img_9.data", dtype=np.uint8).reshape((fheight, fwidth, 3))
R = image[:,:,0]
G = image[:,:,1]
B = image[:,:,2]

#Basically there are some specific functions to reshape the following way, but this one was obviously working
#It's basically just to have the image in the right dimensions [w, h, layers]
p_fits = np.empty((3,fheight, fwidth))
p_fits[0,:,:] = R
p_fits[1,:,:] = G
p_fits[2,:,:] = B
#print(image.shape)

#the step where you can configure your header as wanted
from astropy.io.fits import Header
hdr = Header({'SIMPLE': True, 'XTENSION' : 'IMAGE','BITPIX':8, 'NAXIS':3, 'NAXIS1':image.shape[2],
              'NAXIS2': image.shape[1], 'SIMPLE' :'T', 'CTYPE3':'RGB'    })

#And there fits file is created
output_path = '/'
hdu = fits.PrimaryHDU(p_fits, header = hdr)
hdul = fits.HDUList([hdu])
hdul.writeto(output_path, overwrite=True)
