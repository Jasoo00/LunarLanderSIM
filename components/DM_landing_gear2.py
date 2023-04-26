from base       import *


class DMLandingGear2:

    def __init__(self, DB):

        params = DB.DM["DM_LANDING_GEAR2"]

        self.m       = params["m_0"]
        self.p_c     = array(params["p_c"]   )
        self.p_cg    = array(params["p_cg"]  )
        self.dim     = array(params["dim"]   )

        self.DB      = DB

    
    def update(self):

        pass
