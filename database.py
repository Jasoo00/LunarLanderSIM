from base       import *
from components import *
from lib        import *

class DataBase:


    def __init__(self, inputs):


        ### Quantities ###

        self.m                  = 0                                         # total mass [kg]   : double

        self.I                  = zeros((3,3))                              # inertial matrix   : ndarray(3,3)

        self.p_cg               = zeros(3)                                  # CoG location [m]  : ndarray(3,)


        ### Params ###
        sim_params              = inputs["simulation_params"]               # simulation parameters
        lander_params           = inputs["lander_params"]                   # lunar lander parameters


        ### Simulation Parameters ###
        
        self.rate               = 1/sim_params["PARAM_FRAME"]               # simulation update rate
        self.t                  = 0                                         # simulation time
        self.del_t              = sim_params["PARAM_DELT"]                  # simulation time interval
        self.lat                = deg2rad(sim_params["PARAM_LANDPOINT_LAT"])# land point latitude angle
        self.lon                = deg2rad(sim_params["PARAM_LANDPOINT_LON"])# land point longitude angle


        ### State ###
        self.x                  = array(sim_params["PARAM_INIT_POSE"])      # simulation initial state
        self.x_dot              = zeros(12)                                 # simulation initial state
        self.u                  = zeros(11)                                 # thrusts input [N] : ndarray(11,)


        self.sum_M              = zeros(3)                                  # sum of moments    : ndarray(3,)
        self.sum_F              = zeros(3)                                  # sum of thrusts    : ndarray(3,)

        self.g_M                = 0


        ### Model Parameters ###

        self.AM                 = lander_params["ascent_module"]            # ascent module
        self.DM                 = lander_params["descent_module"]           # descent module

        # Descent Module

        DM_body                 = DMBody                (self)  

        DM_thrust_chamber       = DMThrustChamber       (self)
        DM_fuel_tank            = DMFuelTank            (self)
        DM_oxid_tank            = DMOxidTank            (self)

        DM_landing_gear1        = DMLandingGear1        (self)
        DM_landing_gear2        = DMLandingGear2        (self)
        DM_landing_gear3        = DMLandingGear3        (self)
        DM_landing_gear4        = DMLandingGear4        (self)

        AM_body                 = AMBody                (self)

        AM_RCS1_thrust_chamber1 = AMRCS1ThrustChamber1  (self)
        AM_RCS1_thrust_chamber2 = AMRCS1ThrustChamber2  (self)
        AM_RCS1_thrust_chamber3 = AMRCS1ThrustChamber3  (self)
        AM_RCS1_thrust_chamber4 = AMRCS1ThrustChamber4  (self)
        AM_RCS1_thrust_chamber5 = AMRCS1ThrustChamber5  (self)
        AM_RCS1_fuel_tank       = AMRCS1FuelTank        (self)
        AM_RCS1_oxid_tank       = AMRCS1OxidTank        (self)
        
        AM_RCS2_thrust_chamber1 = AMRCS2ThrustChamber1  (self)
        AM_RCS2_thrust_chamber2 = AMRCS2ThrustChamber2  (self)
        AM_RCS2_thrust_chamber3 = AMRCS2ThrustChamber3  (self)
        AM_RCS2_thrust_chamber4 = AMRCS2ThrustChamber4  (self)
        AM_RCS2_thrust_chamber5 = AMRCS2ThrustChamber5  (self)
        AM_RCS2_fuel_tank       = AMRCS2FuelTank        (self)
        AM_RCS2_oxid_tank       = AMRCS2OxidTank        (self)


        self.components         = [ DM_body                 ,\
                                    DM_thrust_chamber       ,\
                                    DM_fuel_tank            ,\
                                    DM_oxid_tank            ,\
                                    DM_landing_gear1        ,\
                                    DM_landing_gear2        ,\
                                    DM_landing_gear3        ,\
                                    DM_landing_gear4        ,\
                                    AM_body                 ,\
                                    AM_RCS1_thrust_chamber1 ,\
                                    AM_RCS1_thrust_chamber2 ,\
                                    AM_RCS1_thrust_chamber3 ,\
                                    AM_RCS1_thrust_chamber4 ,\
                                    AM_RCS1_thrust_chamber5 ,\
                                    AM_RCS1_fuel_tank       ,\
                                    AM_RCS1_oxid_tank       ,\
                                    AM_RCS2_thrust_chamber1 ,\
                                    AM_RCS2_thrust_chamber2 ,\
                                    AM_RCS2_thrust_chamber3 ,\
                                    AM_RCS2_thrust_chamber4 ,\
                                    AM_RCS2_thrust_chamber5 ,\
                                    AM_RCS2_fuel_tank       ,\
                                    AM_RCS2_oxid_tank]


        # Initialize

        for component in self.components: 
            
            m_i                 = component.m
            p_cgi               = component.p_cg

            ### initial state ###
            r_i                 = self.x[:3]
            O_i                 = self.x[6:9]

            C_i2b               = C_W2B(O_i[0],O_i[1],O_i[2])

            self.g_M            = C_i2b @ (-r_i * G*M/(norm(r_i)**3))




            ### total mass ###
            self.m              += m_i

            ### total cog ###
            self.p_cg           += m_i * p_cgi

            ### inertial matrix ###
            x_cgi               = p_cgi[0]
            y_cgi               = p_cgi[1]
            z_cgi               = p_cgi[2]

            p_cg_X              = array([[0,     -z_cgi,     y_cgi],
                                         [z_cgi,     0,      -x_cgi],
                                         [-y_cgi,    x_cgi,      0]])
                    
            self.I              += p_cg_X @ (-p_cg_X) * m_i

        self.p_cg               = self.p_cg / self.m


    
    def update_quantities(self):

        self.m                  = 0
        self.p_cg               = zeros(3)
        self.I                  = zeros((3,3))

        self.sum_F              = zeros(3)
        self.sum_M              = zeros(3)

        for component in self.components: 

            component.update()
            
            m_i                 = component.m
            p_cgi               = component.p_cg
            F_i                 = component.uvec
            M_i                 = component.Mvec
    
            # print(M_i)

            ### force & moments ###
            self.sum_F          += F_i
            self.sum_M          += M_i

            ### total mass ###
            self.m              += m_i

            ### total cog ###
            self.p_cg           += m_i * p_cgi

            ### inertial matrix ###
            x_cgi               = p_cgi[0]
            y_cgi               = p_cgi[1]
            z_cgi               = p_cgi[2]

            p_cg_X              = array([[0,     -z_cgi,     y_cgi],
                                         [z_cgi,     0,      -x_cgi],
                                         [-y_cgi,    x_cgi,      0]])
            
            self.I              += p_cg_X @ (-p_cg_X) * m_i
            
        self.p_cg               = self.p_cg / self.m

