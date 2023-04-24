from base       import *
from component  import Component


class DMLandingGear2(Component):

    def __init__(self, DB):

        m_0     = DB.components["DM_LANDING_GEAR2"].m_0
        p_c     = DB.components["DM_LANDING_GEAR2"].p_c
        p_cg    = DB.components["DM_LANDING_GEAR2"].p_cg
        dim     = DB.components["DM_LANDING_GEAR2"].dim

        super.__init__(m_0, p_cg, p_c, dim, DB)

    
    def update(self):

        pass
