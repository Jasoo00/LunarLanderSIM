from base       import *


""" DCMs """

def C_I2E(t, lam):

    psi = W_m * t + lam

    R = array([[ cos(psi), sin(psi), 0 ],
               [-sin(psi), cos(psi), 0 ],
               [        0,        0, 1 ]])
    
    return R


def C_E2W(nu):

    theta = pi/2 - nu

    R = array([[ cos(theta),  0,-sin(theta) ],
               [          0,  1,          0 ],
               [ sin(theta),  0, cos(theta) ]])

    return R


def C_W2B(r,p,y):

    R_1 = array([[ 1,      0,      0 ],
                 [ 0, cos(r), sin(r) ],
                 [ 0,-sin(r), cos(r) ]])
    
    R_2 = array([[ cos(p), 0,-sin(p) ],
                 [      0, 1,      0 ],
                 [ sin(p), 0, cos(p) ]])

    R_3 = array([[ cos(y), sin(y), 0 ],
                 [-sin(y), cos(y), 0 ],
                 [      0,      0, 1 ]])
    

    R = R_1@R_2@R_3

    return R


""" Angular Rate Transformation """

def T_w2W(r,p,y):

    R_1 = array([[ 1,      0,      0 ],
                 [ 0, cos(r), sin(r) ],
                 [ 0,-sin(r), cos(r) ]])
    
    R_2 = array([[ cos(p), 0,-sin(p) ],
                 [      0, 1,      0 ],
                 [ sin(p), 0, cos(p) ]])

    R_3 = array([[ cos(y), sin(y), 0 ],
                 [-sin(y), cos(y), 0 ],
                 [      0,      0, 1 ]])

    T_W2w = zeros((3,3))

    T_W2w[:,0] += R_1[:,0]
    T_W2w[:,1] += R_1@R_2[:,1]
    T_W2w[:,2] += R_1@R_2@R_3[:,2]

    try: T_w2W = inv(T_W2w)
    except: 
        T_w2W = eye(3)
        print("*** Singular ***")


    return T_w2W