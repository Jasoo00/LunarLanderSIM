from base       import *


class AMRCS1FuelTank:

    def __init__(self, DB):

        params  = DB.AM["AM_RCS1_FUEL_TANK"]

        self.m_p0    = params["m_p0"]
        self.m_p     = params["m_p0"]
        self.m_s     = params["m_s"]
        self.m       = self.m_p + self.m_s
        self.p_c     = array(params["p_c"]   )
        self.p_cg    = array(params["p_cg"]  )
        self.dim     = array(params["dim"]   )

        self.uvec    = zeros(3)
        self.Mvec    = zeros(3)

        self.I_sp    = DB.AM["AM_RCS1_THRUST_CHAMBER1"]["I_sp"]

        self.DB      = DB


    def update(self):

        F_in         = sum(self.DB.u[1:6])

        self.m_p     = self.m_p - self.DB.del_t * F_in / ( g * self.I_sp )
        self.m       = self.m_p + self.m_s
        
        p_scg        = self.p_c
        p_pcg        = self.p_c - array([ 0, 0, self.dim[0] * ( 1 - self.m_p / self.m_p0 ) ])

        self.p_cg    = (p_scg * self.m_s + p_pcg * self.m_p) / (self.m_p + self.m_s)

        if self.m_p < 0:  

            self.m_p  = 0
            self.p_cg = self.p_c

        else:

            pass

        