from base       import *


class AMBody:

    def __init__(self, DB):

        params = DB.AM["AM_BODY"]

        self.m       = params["m_0"]
        self.p_c     = array(params["p_c"]   )
        self.p_cg    = array(params["p_cg"]  )
        self.dim     = array(params["dim"]   )

        self.uvec    = zeros(3)
        self.Mvec    = zeros(3)

        self.DB      = DB
        

    
    def update(self):

        pass