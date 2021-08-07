# Prototype A

## Physical conception
[add a picture of proto]
Prototype is made of :
- **Environnement** Raspberry Pi 4 8Go [link](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) 
- **Camera Module** Raspberry Pi - Picamera v2.1 [link](https://www.raspberrypi.org/products/camera-module-v2/)
- **IMU** TinkerForge - IMU Brick 2.0 [link](https://www.tinkerforge.com/en/shop/imu-v2-brick.html)
- **Other** : state switches (with 2 positions), cable for IMU (usb-usbA), and the case have been specially designed

## Principle of working
### Data acquisition 

You can either check *Data_collect_CSVIncluded.py* or *Data_collect_NoCSV.py*, the only difference is that in the first
option you will also have a .csv file that enclose IMU data, if you have anything to do with.
Basically it is acquiring orientation (quat/euler), position(LAT,Long, h), time, and information about picture configuration (iso, shutter speed) in a FITS file


### Analysis 

With *error_analysis.py*, it will automatically push your fits file into local version of Astrometry, with only option Source Extractor as extraction process.
It will return some files for each pictures. The most important is wcs file were we can find RA and DEC of pictures.
At the same time, the programm will estimate RA, and DEC from camera boresight axis, regarding GPS information, time, and IMU orientation.
Finally, it will returns a .txt file with sucess rate of your try, and mean, min, max, and std of RA error and DEC error.

### Run Boot
In case, you can't find any screen or not enough power supply where you're running your test, you can with *run_at_boot.py* and README steps,
run the program at the boot, or allow it to run with no screen. 
However, modifying boot process can result of RPi disfunctionment.