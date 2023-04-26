from base       import *

from components import *
from database   import DataBase


class Simulator:


    def __init__(self, inputs):

        ### Initialize ###
        self.DB = DataBase(inputs)




if __name__ == "__main__":


    inputs_path = "inputs.json"

    with open(inputs_path,'r') as inps:

        inputs = json.load(inps)

        SIM = Simulator(inputs)

