# Lost In Space Approach

##Astrometry
There you can find the code that allow automatic use of astrometry with python.
It is simply building a command line and pushing it to the Linux Terminal.
Then Astrometry is running by itself.
If you want to download Astrometry please refer [official page](https://nova.astrometry.net/api_help)

##FITS file creation from .data files
As Astrometry is considering a short list of files (TIF, FITS, png), pictures had to be converted.
FITS file looks the best options as it can onboard header with informations, easyli accesible.
The **FITS_Converting&Manipulation.py file** shows how it has been done, in our case.

##Example
Please also find attached some pictures that has been taken during some of test.
Pictures with '_Rennes'has been shoot with Picamera v2.1, ISO was around 200 for these which success and shutter_speed either 1,5 or 2s
Also you have, the output from astrometry so basicaaly you have the extracted sources, the stars used for matching, and constellations that appears on the input image.
you also have a wcs file, with informations about RA/ DEC, and transformations