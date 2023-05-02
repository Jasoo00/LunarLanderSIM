from base   import *
from lib.transformations    import *


def f(x, t, DB):

    r_i       = x[:3]
    v_b       = x[3:6]
    O_i       = x[6:9]
    w_b       = x[9:12]

    C_i2b     = C_W2B(O_i[0],O_i[1],O_i[2])
    T_b2i     = T_w2W(O_i[0],O_i[1],O_i[2])

    sum_F     = DB.sum_F
    sum_M     = DB.sum_M


    g_M       = C_i2b @ (-r_i * G*M/(norm(r_i)**3))

    r_i_dot   = C_i2b.T @ v_b
    
    v_b_dot   = g_M + (1/DB.m) * sum_F - cross(w_b, v_b)

    O_i_dot   = T_b2i @ w_b

    w_b_dot   = inv(DB.I) @ ( sum_M - cross(w_b,(DB.I @ w_b)) )

    x_dot     = zeros(12)

    x_dot[:3]   = r_i_dot
    x_dot[3:6]  = v_b_dot
    x_dot[6:9]  = O_i_dot
    x_dot[9:12] = w_b_dot

    DB.x_dot    = x_dot
    DB.g_M      = g_M

    # print("sum_M",sum_M)
    # print("w_b_dot",w_b_dot)
    # print("w_b",w_b)
    # print("O_i",O_i)
    return x_dot


def update_state(DB):

    ang_lim = 10

    ### RK4 Integration ###
    x_1     = DB.x

    h       = DB.del_t
    K1      = f(x_1,0, DB)
    K2      = f(x_1 + 0.5*h*K1,0, DB)
    K3      = f(x_1 + 0.5*h*K2,0, DB)
    K4      = f(x_1 + h*K3,0, DB)

    x_2     = x_1 + (h/6)*(K1 + 2*K2 + 2*K3 + K4)

    DB.x    = x_2