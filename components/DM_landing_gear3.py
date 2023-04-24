from base       import *
from component  import Component


class DMLandingGear3(Component):

    def __init__(self, DB):

        m_0     = DB.components["DM_LANDING_GEAR3"].m_0
        p_c     = DB.components["DM_LANDING_GEAR3"].p_c
        p_cg    = DB.components["DM_LANDING_GEAR3"].p_cg
        dim     = DB.components["DM_LANDING_GEAR3"].dim

        super.__init__(m_0, p_cg, p_c, dim, DB)

    
    def update(self):

        pass