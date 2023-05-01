from base       import *


class DMFuelTank:

    def __init__(self, DB):

        params  = DB.DM["DM_DE_FUEL_TANK"]

        self.m_p0    = params["m_p0"]
        self.m_p     = params["m_p0"]
        self.m_s     = params["m_s"]
        self.m       = self.m_p + self.m_s
        self.p_c     = array(params["p_c"]   )
        self.p_cg    = array(params["p_cg"]  )
        self.dim     = array(params["dim"]   )

        self.I_sp    = DB.DM["DM_DE_THRUST_CHAMBER"]["I_sp"]

        self.DB      = DB


    def update(self):

        F_in         = self.DB.u[0]

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