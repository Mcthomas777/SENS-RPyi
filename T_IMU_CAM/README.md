# Kalibr IMU/Cam Calibration

## Installation

To run Kalibr, you can either use cde-package, or download ROS(works with Indigo, and Melodic) on Ubuntu(14.4 is necessary for Indigo and 
16.6 for Melodic). For more detailled installation please refer [Kalibr](https://github.com/ethz-asl/kalibr)

**Here Kalibr has been run with Indigo, and Ubuntu 14.4**

Make sure your created, and set up your work environnement. And then use the following line, before running any command:
'<source ~/kalibr_workspace/devel/setup.bash>'

## .bag File manipulation

1) Extraction 

'<kalibr_bagextractor --image-topics /cam0/image_raw  --imu-topics /imu0 --output-folder dataset-dir --bag full_path_2_bag/bag_name.bag >'

with : --bag, the file you want to extract the file from
       --output-folder, the file you want to extract data to 

2) Creation

'<kalibr_bagcreater --folder dataset-dir --output-bag awsome.bag>'

with : --folder, the file you want to put in .bag format
       --output-bag, the name of the bag, you can set the path where you want to create it


## IMU_CAM_Calibration

[**Camera calibration**](https://github.com/ethz-asl/kalibr/wiki/multiple-camera-calibration) :

'<rosrun kalibr kalibr_calibrate_cameras --bag path_2_bag/bag_file.bag --model pinhole-radtan --target path/calibration_grid.yaml --topic /cam0/image_raw>'

**IMU/Cam Calibration can be run with**:

'<kalibr_calibrate_imu_camera --target path/calibration_pattern.yaml --cam path/camchain.yaml --imu path/imu_Brick.yaml --bag path/dynamic.bag --bag-from-to 5 45>'

## Other 

In the examples file, there are camera, IMU, and calibration pattern specs for the used materials (IMU BRICK 2.0 (TForge), et Rpi - Picamera v2.1)
Also, you can find the output files of the calibration, so informations about choosen configuration, T_ic (Transformation matrix), and a pdf file with a bunch of diagrams that can be usefull to deeply understand the reliability and the efficiency of calibration.

For example, you have these kind of reprojection error plot :
### Example Plot - Reprojection error - Resolution (2048*1472 [4:3]) & python output
![Reprojection error](T_IMU_CAM/Examples/Results/Repro_e.PNG)
 



