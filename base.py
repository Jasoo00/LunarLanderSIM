### libraries ###
import os
import json
import time
import warnings

from    numpy                   import  array, zeros, ones, linspace,\
                                        outer, size, cross, vstack, hstack,\
                                        deg2rad, rad2deg, cos, sin, tan, pi
from    numpy.linalg            import  inv, norm
from    threading               import  Thread
from    mpl_toolkits.mplot3d    import  Axes3D
import  matplotlib.pyplot       as      plt




M = 7.36e22         # mass of the moon
G = 6.67e-11        # gravity constant
g = 9.81            # General gravity acceleration
T_m = 27.3*24*3600  # revolution period of the moon
W_m = 2*pi/T_m      # rotation velocity of the moon