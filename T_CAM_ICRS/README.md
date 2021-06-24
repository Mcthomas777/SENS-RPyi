# T_CAM_ICRS

In this part, we will deal with different problematics : the choice of stars catalogue, the determination of limit magnitude, and the study of positioning error regarding different parameters.

## Choice of star catalogue 

In this part, we're using astropy.table mainly, to manipulate catalogue as table. From this, we are able to manage data as wished.
We can, for example, see the stars repartition on the celestial frame for a special magnitude, in a Mollweide projection. 
You can also display cumulative histogram and, and table, so you can check number of stars, names, different magnitude and attitude.

## Determination of limit magnitude

This part is a bit more tricky as the experiment was run with specific tools. In my case, I used something call a colimator, 
which is an optic system, that with some specific mirror configuration is able to reproduce an infinite point, and equivalence of star.
You can change magnitude by using filters that allow to reduce or increase the light flow, and even the color of your star.

![Colimator](T_CAM_ICRS/Limit_magnitude/Colim.jpg)

Basically the program, does not that much, it is mainly used to take some pictures with different ISO and exposure time configuration, in a raw RGB format, so without compression.
You can ajust the program either to manage both or only one parameters. And you also have histogram functions for each R,G,B layer, and also in gray. Last function, is made to display different pictures regarding different parameters, but as the star is a tiny part of the picture it's not that visible

## Study of localisation error 

For the localisation error, it is based on a [publication](https://ieeexplore.ieee.org/document/1008988).
Objective is to understand the impact of different parameters as number of detectable stars, field of view, number of pixel, and centroid error.


 

