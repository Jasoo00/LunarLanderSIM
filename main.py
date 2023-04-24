from base       import *

from components import *
from database   import DataBase


class LunarLanderSIM:


    def __init__(self, inputs):

        self.DB = DataBase(inputs)

        DM_body             = DMBody            (self.DB)
        DM_thrust_chamber   = DMThrustChamber   (self.DB)
        DM_fuel_tank        = DMFuelTank        (self.DB)
        DM_oxid_tank        = DMOxidTank        (self.DB)
        DM_landing_gear1    = DMLandingGear1    (self.DB)
        DM_landing_gear2    = DMLandingGear2    (self.DB)
        DM_landing_gear3    = DMLandingGear3    (self.DB)
        DM_landing_gear4    = DMLandingGear4    (self.DB)

        


if __name__ == "__main__":

    inputs = "inputs.json"

