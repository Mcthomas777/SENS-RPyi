# T_gl_IMU
This part is made to understand the functionment and the convention of the IMU, understand principle of Scipy.Rotation,
and getting a first idea of how the transformation between the different frame should be realized.

## *quat_vs_euler.py* :

Try to get the same angle and a 0 magnitude between same rotation in euler and in quat.
It is returning both euler, and quat convert to euler angle and magnitude of rotation composition

## *Deriv_if_IMU_with_magnitude.py* :

Register all the orientation during a defined amount of time, then plotting evolution of the error in arcsec, 
regarding magnitude between first and last i-rotation. 
You can either change the code to record automatically, and to see derivation along time, or configure it to see the derivation of the 
IMU after being shake.
As I was not using a 3-axis table, result is obviously not that reliable, because I'm not coming at the exact same position.

## *find_RA_DEC_pred.py* :

To adjust your transformation between geographic frame, and camera frame. It means finding orientation of camera in geographic frame, that require 
GPS information, and a some determination, because each system have different frame, different convention. IMU Brick is a bit messy for that
it use a special convention, and as it is strapped down to my it is even more complicate. So GOOD Luck to you
  