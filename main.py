from base       import *

from components import *
from database   import DataBase


class LunarLanderSIM:


    def __init__(self, inputs):

        self.DB = DataBase(inputs)

        # sim_params          = inputs["simulation_params"]
        # lander_params       = inputs["lander_params"]

        # ### Simulation Parameters ###
        
        # self.del_t          = sim_params["PARAM_DELT"]
        # self.x_init         = sim_params["PARAM_INIT_POSE"]

        # ### Model Parameters ###

        # self.AM             = lander_params["ascent_module"]
        # self.DM             = lander_params["descent_module"]

        # # Descent Module


        # DM_body             = DMBody            (self.DB)
        # DM_thrust_chamber   = DMThrustChamber   (self.DB)
        # DM_fuel_tank        = DMFuelTank        (self.DB)
        # DM_oxid_tank        = DMOxidTank        (self.DB)
        # DM_landing_gear1    = DMLandingGear1    (self.DB)
        # DM_landing_gear2    = DMLandingGear2    (self.DB)
        # DM_landing_gear3    = DMLandingGear3    (self.DB)
        # DM_landing_gear4    = DMLandingGear4    (self.DB)

        


if __name__ == "__main__":



    inputs_path = "inputs.json"

    with open(inputs_path,'r') as inps:

        inputs = json.load(inps)

        SIM = LunarLanderSIM(inputs)