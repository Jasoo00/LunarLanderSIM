from base       import *
from component  import Component


class DMThrustChamber(Component):

    def __init__(self, DB):

        m_0     = DB.components["DM_THRUST_CHAMBER"].m_0
        p_c     = DB.components["DM_THRUST_CHAMBER"].p_c
        p_cg    = DB.components["DM_THRUST_CHAMBER"].p_cg
        dim     = DB.components["DM_THRUST_CHAMBER"].dim

        super.__init__(m_0, p_cg, p_c, dim, DB)

    
    def update(self):

        pass
