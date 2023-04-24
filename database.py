from components import *
from base       import *


class DataBase:


    def __init__(self, inputs_path):

        with open(inputs_path,'r') as inps:

            inputs = json.load(inps)

            sim_params          = inputs["simulation_params"]
            lander_params       = inputs["lander_params"]

            ### Simulation Parameters ###
            
            self.del_t          = sim_params["PARAM_DELT"]
            self.x_init         = sim_params["PARAM_INIT_POSE"]

            ### Model Parameters ###

            self.AM             = lander_params["ascent_module"]
            self.DM             = lander_params["descent_module"]

            # Descent Module

            self.DM_body             = DMBody            (self)
            self.DM_thrust_chamber   = DMThrustChamber   (self)
            self.DM_fuel_tank        = DMFuelTank        (self)
            self.DM_oxid_tank        = DMOxidTank        (self)
            self.DM_landing_gear1    = DMLandingGear1    (self)
            self.DM_landing_gear2    = DMLandingGear2    (self)
            self.DM_landing_gear3    = DMLandingGear3    (self)
            self.DM_landing_gear4    = DMLandingGear4    (self)


            # States

            self.m              = 
