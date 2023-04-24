from base       import *
from component  import Component


class DMOxidTank(Component):

    def __init__(self, DB):

        m_0     = DB.components["DM_OXID_TANK"].m_0
        p_c     = DB.components["DM_OXID_TANK"].p_c
        p_cg    = DB.components["DM_OXID_TANK"].p_cg
        dim     = DB.components["DM_OXID_TANK"].dim

        super.__init__(m_0, p_cg, p_c, dim, DB)

    
    def update(self):

        F_in = self.DB.components["DM_THRUST_CHAMBER"].F_in
        I_sp = self.DB.components["DM_THRUST_CHAMBER"].I_sp
        m_p0 = self.DB.components["DM_OXID_TANK"].m_p0
        m_p  = self.DB.components["DM_OXID_TANK"].m_p
        m_s  = self.DB.components["DM_OXID_TANK"].m_s

        m_p    = m_p - self.DB.del_t * F_in / ( 9.81 * I_sp )
        
        p_scg = self.p_c
        p_pcg = self.p_c - array([ 0, 0, self.dim[0] * ( 1 - m_p / m_p0 ) ])

        p_cg = p_scg * m_s + p_pcg * m_p

        if m_p < 0:  

            self.DB.components["DM_OXID_TANK"].m_p  = 0
            self.DB.components["DM_OXID_TANK"].p_cg = self.p_c

        else:

            self.DB.components["DM_OXID_TANK"].m_p  = m_p
            self.DB.components["DM_OXID_TANK"].p_cg = p_cg
