##Camera Calibration

To match with Kalibr requirement, we need to find out the intrinsinc parameters, and distortion coefficient.
This is the reason why a camera calibration is helpfull.

**Hardware :** Raspberry Pi - Picamera v2.1

**Process :**

1) Create your data set. You will need a specific grid, you can either use checkerboard, april grid or circle grid.
   Once you have yours, just take a bunch of pictures (50-200, number does not mean more realiable result), moving the grid around the fixed camera and trying to cover your entire field of view.
   You can juste use the python code (using opencv) images_4calib2.py
	
*Warning* : Don't try to change the distance significantly, and avoid large rotation of the grid.

2) Either use camera_calib2.py or [Kalibr Multiple Camera Calibration tools](https://github.com/ethz-asl/kalibr)
   The first option does not require any other dependancies installation, but the Kalibr tool edit reprojection error diagram, which help to understand a lot what is happening during calibration, and also edit a .yaml file that is compatible 
   with Kalibr IMU/CAM calibration tools.

