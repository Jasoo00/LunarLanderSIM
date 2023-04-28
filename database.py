from base       import *
from components import *
from lib        import *

class DataBase:


    def __init__(self, inputs):


        ### States ###

        self.m              = 0                                         # total mass [kg]   : double

        self.I              = zeros((3,3))                              # inertial matrix   : ndarray(3,3)

        self.p_cg           = zeros(3)                                  # CoG location [m]  : ndarray(3,)

        self.u              = zeros(11)                                 # thrusts [N]       : ndarray(11,)

        self.M              = zeros(3)                                  # sum of moments    : ndarray(3,)


        ### Params ###
        sim_params          = inputs["simulation_params"]               # simulation parameters
        lander_params       = inputs["lander_params"]                   # lunar lander parameters


        ### Simulation Parameters ###
        
        self.t              = 0                                         # simulation time
        self.del_t          = sim_params["PARAM_DELT"]                  # simulation time interval
        self.x              = array(sim_params["PARAM_INIT_POSE"])      # simulation initial state
        self.lat            = deg2rad(30)                               # land point latitude angle
        self.lon            = deg2rad(30)                               # land point longitude angle

        ### Model Parameters ###

        self.AM             = lander_params["ascent_module"]            # ascent module
        self.DM             = lander_params["descent_module"]           # descent module

        # Descent Module

        DM_body             = DMBody            (self)
        DM_thrust_chamber   = DMThrustChamber   (self)
        DM_fuel_tank        = DMFuelTank        (self)
        DM_oxid_tank        = DMOxidTank        (self)
        DM_landing_gear1    = DMLandingGear1    (self)
        DM_landing_gear2    = DMLandingGear2    (self)
        DM_landing_gear3    = DMLandingGear3    (self)
        DM_landing_gear4    = DMLandingGear4    (self)


        self.components     = [ DM_body,\
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


    
    def update_quantities(self):

        self.m = 0
        self.p_cg = zeros(3)
        self.I = zeros((3,3))

        for component in self.components: 

            component.update()
            
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



    def update_state(self):

        r_i_1     = self.x[:3]
        v_b_1     = self.x[3:6]
        O_i_1     = self.x[6:9]
        w_b_1     = self.x[9:12]

        C_i2e     = C_I2E(self.t, self.lon)
        C_e2w     = C_E2W(self.lat)
        C_i2b     = C_W2B(O_i_1[0],O_i_1[1],O_i_1[2])
        T_b2i     = T_w2W(O_i_1[0],O_i_1[1],O_i_1[2])

        sum_F     = array([ self.u[6]-self.u[1], \
                            self.u[2]-self.u[3]+self.u[7]-self.u[8], \
                            self.u[4]-self.u[5]+self.u[8]-self.u[10]+self.u[0]])

        sum_M     = zeros(3)

        ###  ###
        r_i_2     = r_i_1 + self.del_t * (C_i2b.T @ v_b_1)
        
        v_b_2     = v_b_1 + self.del_t * ( C_i2b @ (-r_i_1 * G*M/(norm(r_i_1)**3)) + \
                    (1/self.m) * sum_F )

        O_i_2     = O_i_1 + self.del_t * (T_b2i @ w_b_1)

        w_b_2     = w_b_1 + self.del_t * ( inv(self.I) @ ( sum_M - cross(w_b_1,(self.I@w_b_1)) ) )

        self.x[:3]      = r_i_2
        self.x[3:6]     = v_b_2
        self.x[6:9]     = O_i_2
        self.x[9:12]    = w_b_2        

