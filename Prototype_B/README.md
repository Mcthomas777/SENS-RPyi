# Prototype B
## What's new ?

- **IHM** : SENS-RPYi now embedded a TinkerForge IHM, with a digital LCD touch screen.	
	You can select different parameters (ISO, exposure time) value for the camera with slider.
	Choose if you'd rather save .csv fileor not, if you'd rather do Darks, if you want to do another session.
	It also allow you to estimate the attitude of boresight axis, then you approximately know what will be the camera shooting.
	Finally, it embedded a real time interface, that return number of pictures, current temperature and pressure.
	You can interrupt the test whenever you want by pressing the button.

- **Barometer/ Thermometer**: Having temperature and pressure is not interesting when you're taking pictures of the stars. However, a phenomen
	is happening regarding different pressure or temperature, it is called *atmospheric refraction* that generate a deviation of optical path.

- **Camera Module**: Major improvement for the systems, the new chosen camera module is made of the camera sensor, Picamera HQ,
	with a bigger sensor size, and bigger size pixel, also it is a BackSide illuminated sensor. Mainly, it means more signal, and less noise, so a bigger SNR.
	Along with the new sensor, comes a new lens/objective. It is an accesible 16mm focal lenght objective, that is compatible with Picamera HQ. Despite we can have better quality objectives,
	and bigger focal lenght, 16mm was a good options (50 euros) and also the field of view remains 30°  wide, which is pretty good in our case.

- **AStrometry** : COMMING SOON