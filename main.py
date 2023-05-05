from base               import *
from components         import *
from lib                import *

from database           import DataBase
from visualizer         import Visualizer
from physics_engine     import PhysicsEngine


class Simulator:


    def __init__(self, inputs):

        ### Initialize ###
        self.DB     = DataBase      (inputs)
        self.viz    = Visualizer    (self.DB)
        self.PE     = PhysicsEngine (self.DB)

        self.PE.start()
        self.viz.run()


if __name__ == "__main__":


    inputs_path = "inputs.json"

    with open(inputs_path,'r') as inps:

        inputs = json.load(inps)

        SIM = Simulator(inputs)

