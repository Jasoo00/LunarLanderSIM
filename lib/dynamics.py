from base   import *
from lib    import *


def f(x, t, DB):

    r_i       = x[:3]
    v_b       = x[3:6]
    O_i       = x[6:9]
    w_b       = x[9:12]

    C_i2e     = C_I2E(t, DB.lon)
    C_e2w     = C_E2W(DB.lat)
    C_i2b     = C_W2B(O_i[0],O_i[1],O_i[2])
    T_b2i     = T_w2W(O_i[0],O_i[1],O_i[2])

    sum_F     = array([ DB.u[6]-DB.u[1], \
                        DB.u[2]-DB.u[3]+DB.u[7]-DB.u[8], \
                        DB.u[4]-DB.u[5]+DB.u[8]-DB.u[10]+DB.u[0]])

    sum_M     = zeros(3)

    ###  ###
    r_i_dot   = C_i2b.T @ v_b
    
    v_b_dot   = C_i2b @ (-r_i * G*M/(norm(r_i)**3)) + \
                (1/DB.m) * sum_F

    O_i_dot   = T_b2i @ w_b

    w_b_dot   = inv(DB.I) @ ( sum_M - cross(w_b,(DB.I@w_b)) )

    x_dot     = zeros(12)

    x_dot[:3]   = r_i_dot
    x_dot[3:6]  = v_b_dot
    x_dot[6:9]  = O_i_dot
    x_dot[9:12] = w_b_dot

    return x_dot