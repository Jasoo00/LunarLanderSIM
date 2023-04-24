from base import *



class Component:


    def __init__(self, m_0, p_cg, p_c, dim, DB):

        self.DB     = DB

        self.m_0 = m_0
        self.p_cg = p_cg
        self.p_c = p_c
        self.dim = dim


    def update(self):

        return NotImplementedError()