# RPyi-SENS

This GitHub has been created for project RPyi - SENS, that stand for Raspberry Pi / Py - Stars Extraction Navigation System. <br />
As it is called, system will have to refind its attitude regarding stars position at a t-time, attitude of the holder must been has precise as it can, 
regarding the technologies used. <br />

If any questions, contact : j.thomas15@outlook.fr


## 1) What the purposes ?

Using mainly python, and some other hardwares that will be detailled in the part Hardware, what we want to do is basically find the position of our system (local frame) in the earth frame (so using coordinates in terms of longitude and latitude). <br />
To reach this point, we are going to switch frame over and over, from the body frame, to the ICRS (J2000), to the earth frame... 
For each frame switching, there are specific task that we will have to deal with :

  1) from Camera to ICRS : We will try to solve the Lost In Space Approach (LISA) with astrometry.net 
  2) from ICRS to earth : Using GPS time, and earth speed rotation
  3) from Local to IMU : Euler's angle (yaw, pitch, roll) determinated by IMU
  4) from IMU to Camera : We will use kalibr to run a proper calibration of our IMU and camera.

Each process is engaging other process, for example : For IMU to camera, we will need to calibrate camera, and to evaluate error model of IMU. However, this will be detailled in each individual frame switching file.


## 2) Hardware used :

To run the first prototype, it has been decided to use the following hardware :

- Raspberry Pi 4, 8Go : As it was about to do some images and calculation processing, and as I was beginner in all of this, I decided to use easy interface, and flexibility  and power of Raspbery Pi.
- Raspberry Cam V2.1 Module camera : That is a cheap camera, with integrated lens, so we can't change that much parameters. It is possible to change with Raspberry Cam HQ Module camera, which embed CS/C - mount technologies
and allow us to have a better flexibility regarding lens choice, with better CMOS sensor, and better image format.
- IMU Brick 2.0 (TinkerForge) : That is a low-cost inertial measurement unit, but that offer us a good range of functions, an easy interface thanks to TinkerForge and its properties are enough as I will use it for personnal purposes.
- GPS (DIYMall) G-mouse : The positionning system is not that necessary as we are searching for this position, but it will be very usefull as a clock as the one of the raspberry is not that good. We also want to use it, to characterized the error of our system.
  
