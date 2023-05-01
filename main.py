from base       import *

from components import *
from lib        import *
from database   import DataBase
from visualizer import Visualizer


class Simulator:


    def __init__(self, inputs):

        ### Initialize ###
        self.DB     = DataBase(inputs)
        self.viz    = Visualizer(self.DB)

        self.viz.start()

        while True:

            self.DB.update_quantities()
            
            update_state(self.DB)

            time.sleep(0.01)
            
            self.DB.t += self.DB.del_t


if __name__ == "__main__":


    inputs_path = "inputs.json"

    with open(inputs_path,'r') as inps:

        inputs = json.load(inps)

        SIM = Simulator(inputs)

