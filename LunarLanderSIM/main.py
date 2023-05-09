from base               import *
from components         import *
from lib                import *

from database           import DataBase
from physics_engine     import PhysicsEngine
from visualizer         import Visualizer
from communicator       import Communicator


class Simulator:


    def __init__(self, inputs):

        ### Initialize ###
        self.DB     = DataBase      (inputs)
        self.viz    = Visualizer    (self.DB)
        self.PE     = PhysicsEngine (self.DB)
        self.com    = Communicator  (self.DB)

        self.PE.start()
        self.viz.run()


if __name__ == "__main__":


    inputs_path = "inputs.json"

    with open(inputs_path,'r') as inps:

        inputs = json.load(inps)

        SIM = Simulator(inputs)

