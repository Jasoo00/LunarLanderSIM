import os
import json

from    numpy               import  array, zeros, ones, linspace,\
                                    outer, size,\
                                    deg2rad, rad2deg, cos, sin, tan, pi, arccos, dot

import  matplotlib.pyplot   as      plt

M = 10e4            # mass of the moon
G = 1               # gravity constant
g = 9.81            # General gravity acceleration
T_m = 27.3*24*3600  # revolution period of the moon
W_m = 2*pi/T_m      # rotation velocity of the moon