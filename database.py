from components import *
from base       import *


class DataBase:


    def __init__(self, inputs):


        ### States ###

        self.m              = 0             # total mass [kg]   : double

        self.I              = zeros((3,3))  # inertial matrix   : ndarray(3,3)

        self.p_cg           = zeros(3)      # CoG location [m]  : ndarray(3,)

        self.u              = zeros(11)     # thrusts [N]       : ndarray(11,)


        ### Params ###
        sim_params          = inputs["simulation_params"]
        lander_params       = inputs["lander_params"]


        ### Simulation Parameters ###
        
        self.del_t          = sim_params["PARAM_DELT"]
        self.x              = sim_params["PARAM_INIT_POSE"]

        ### Model Parameters ###

        self.AM             = lander_params["ascent_module"]
        self.DM             = lander_params["descent_module"]

        # Descent Module

        DM_body             = DMBody            (self)
        DM_thrust_chamber   = DMThrustChamber   (self)
        DM_fuel_tank        = DMFuelTank        (self)
        DM_oxid_tank        = DMOxidTank        (self)
        DM_landing_gear1    = DMLandingGear1    (self)
        DM_landing_gear2    = DMLandingGear2    (self)
        DM_landing_gear3    = DMLandingGear3    (self)
        DM_landing_gear4    = DMLandingGear4    (self)


        self.components     = [DM_body,\
                                DM_thrust_chamber,\
                                DM_fuel_tank,\
                                DM_oxid_tank,\
                                DM_landing_gear1,\
                                DM_landing_gear2,\
                                DM_landing_gear3,\
                                DM_landing_gear4]


        # Initialize

        for component in self.components: 
            
            m_i     = component.m
            p_cgi   = component.p_cg

            ### total mass ###
            self.m += m_i

            ### total cog ###
            self.p_cg += m_i * p_cgi

            ### inertial matrix ###
            x_cgi   = p_cgi[0]
            y_cgi   = p_cgi[1]
            z_cgi   = p_cgi[2]

            p_cg_X = array([[0,     -z_cgi,     y_cgi],
                            [z_cgi,     0,      -x_cgi],
                            [-y_cgi,    x_cgi,      0]])
            
            self.I += p_cg_X @ (-p_cg_X) * m_i

        self.p_cg = self.p_cg / self.m

        print(self.m)
        print(self.p_cg)
        print(self.I)
