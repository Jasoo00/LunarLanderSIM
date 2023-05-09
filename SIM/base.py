import os
import json
import time

### Numpy libraries ###
from    numpy                   import  array, zeros, ones, eye, empty, linspace,\
                                        where, size, outer, cross, concatenate, reshape,\
                                        deg2rad, rad2deg, cos, sin, tan, pi
from    numpy.linalg            import  inv, norm

### Visualiser libraries ###
from    mpl_toolkits.mplot3d    import  Axes3D
from    matplotlib.animation    import  FuncAnimation
import  matplotlib.pyplot       as      plt

### Threading library ###
from    threading               import  Thread

### ROS libraries ###
import  rospy
from std_msgs.msg               import Float32MultiArray



M = 7.36e22         # mass of the moon
G = 6.67e-11        # gravity constant
g = 9.81            # General gravity acceleration
T_m = 27.3*24*3600  # revolution period of the moon
W_m = 2*pi/T_m      # rotation velocity of the moon
R_m = 1.737e6       # radius of the moon