import math as m
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


class Dynamics:
    
    def __init__(self, statevariables):

        sim_sv                = statevariables["simulation_params"]
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

        pose0        = [self.x0, self.y0, self.z0]
        pose         = [self.x, self.y, self.z]
        angle0       = [self.phi0, self.theta0, self.psi0]
        angle0       = [self.phi, self.theta, self.psi]
        vel0         = [self.u0, self.v0, self.w0]
        vel          = [self.u, self.v, self.w]
        angle_vel0   = [self.p0, self.q0, self.r0]
        angle_vel    = [self.p, self.q, self.r]

        DCM = array[[m.cos(self.theta0)*m.cos(self.psi0), m.sin(self.phi0)*m.sin(self.theta0)*m.cos(self.psi0)-m.cos(self.phi0)*m.sin(self.psi0), m.cos(self.phi0)*m.sin(self.theta0)*m.cos(self.psi0)+m.sin(self.phi0)*m.sin(self.psi0)],
                    [m.cos(self.theta0)*m.sin(self.psi0), m.sin(self.phi0)*m.sin(self.theta0)*m.sin(self.psi0)+m.cos(self.phi0)*m.cos(self.psi0), m.cos(self.phi0)*m.sin(self.theta0)*m.sin(self.psi0)-m.sin(self.phi0)*m.cos(self.psi0)],
                    [-m.sin(self.theta0), m.sin(self.phi0)*m.cos(self.theta0), m.cos(self.phi0)*m.cos(self.theta0)]]
        

        def pose_fn(ode_fn_pose):
            return ode_fn_pose
        
        ode_fn_pose = lambda t , pose : DCM @ pose0
        t = np.arange(0, 500, 0.1)
        pose = solve_ivp(ode_fn_pose, [0, 500], [self.u0, self.v0, self.w0], t_eval=np.linspace[0, 500, 5000])
        plt.plot(t, pose[1])
        plt.show(t, pose[1])






        
        


        

    





