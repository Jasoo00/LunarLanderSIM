import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from base          import *
from database      import DataBase
from scipy.integrate import odeint

class Dynamics:
    
    def __init__(self, DB):

        self.DB               = DB
        self.m                = DB.m  # mass
        self.I                = DB.I  # moment of inertia
        self.u                = DB.u  # F
        self.M                = DB.M  # Moment

        sim_sv                = DB["simulation_params"]
        self.dt               = sim_sv["PARAM_DELT"]  
        self.sv               = sim_sv["PARAM_INIT_POSE"]

        self.x0               = sim_sv[0],  self.x        = self.x0
        self.y0               = sim_sv[1],  self.y        = self.y0
        self.z0               = sim_sv[2],  self.z        = self.z0
        self.phi0             = sim_sv[3],  self.phi      = self.phi0
        self.theta0           = sim_sv[4],  self.theta    = self.theta0
        self.psi0             = sim_sv[5],  self.psi      = self.psi0
        self.u0               = sim_sv[6],  self.u        = self.u0
        self.v0               = sim_sv[7],  self.v        = self.v0
        self.w0               = sim_sv[8],  self.w        = self.w0
        self.p0               = sim_sv[9],  self.p        = self.p0
        self.q0               = sim_sv[10], self.q        = self.q0
        self.r0               = sim_sv[11], self.r        = self.r0

        pose                  = [self.x, self.y, self.z]
        angle                 = [self.phi, self.theta, self.psi]
        vel                   = [self.u, self.v, self.w]
        angle_vel             = [self.p, self.q, self.r] 

        DCM     = array[[cos(self.theta)*cos(self.psi), sin(self.phi)*sin(self.theta)*cos(self.psi)-cos(self.phi)*sin(self.psi), cos(self.phi)*sin(self.theta)*cos(self.psi)+sin(self.phi)*sin(self.psi)],
                        [cos(self.theta)*sin(self.psi), sin(self.phi)*sin(self.theta)*sin(self.psi)+cos(self.phi)*cos(self.psi), cos(self.phi)*sin(self.theta)*sin(self.psi)-sin(self.phi)*cos(self.psi)],
                        [-sin(self.theta)             , sin(self.phi)*cos(self.theta)                                          , cos(self.phi)*cos(self.theta)]]
        
        TM      = array[[1, sin(self.phi)*tan(self.theta)   ,  cos(self.phi)*tan(self.theta)],
                        [0, cos(self.phi)                   , -sin(self.phi)],
                        [0, sin(self.phi)*arccos(self.theta),  cos(self.phi)*arccos(self.theta)]] 
            
        VM      = -angle_vel @ vel
        AVM     = dot(inv(DB.I), [-angle_vel @ dot(DB.I, angle_vel)])
        
        FM      = DB.u/DB.m
        MM      = dot(inv(DB.I), DB.M)

        state_k = [[self.x], [self.y], [self.z], [self.phi], [self.theta], [self.psi], [self.u], [self.v], [self.w], [self.p], [self.q], [self.r]]
        input   = [[0],[0],[0],[0],[0],[0],[FM[1]],[FM[2]],[FM[3]],[MM[1]],[MM[2]],[MM[3]]]



        def state_eq(state_k, t, input):
            
            A       = array[[0, 0, 0, 0, 0, 0, DCM[1,1], DCM[1,2], DCM[1,3], 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, DCM[2,1], DCM[2,2], DCM[2,3], 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, DCM[3,1], DCM[3,2], DCM[3,3], 0, 0, 0], 
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, TM[1,1], TM[1,2], TM[1,3]],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, TM[2,1], TM[2,2], TM[2,3]],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, TM[3,1], TM[3,2], TM[3,3]],
                            [0, 0, 0, 0, 0, 0, VM[1]/self.u, 0           , 0,            0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0           , VM[2]/self.v, 0,            0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0           , 0           , VM[3]/self.w, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0,  AVM[1]/self.p, 0            , 0            ],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,              AVM[2]/self.q, 0            ],  
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0          , 0            , AVM[3]/self.r]]
            
            B       = np.diag(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

            state_dot = dot(A, state_k) + dot(B, input)
            
            return state_dot     

        t_span = np.linspace(0, 500, 5000)
        state = odeint(state_eq, state_k, t_span, args=(input,))