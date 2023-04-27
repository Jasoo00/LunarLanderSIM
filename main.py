from base       import *

from components import *
from database   import DataBase
import matplotlib.pyplot as plt


class Simulator:


    def __init__(self, inputs):

        ### Initialize ###
        self.DB = DataBase(inputs)




if __name__ == "__main__":

    plt.figure()
    plt.show()

    inputs_path = "inputs.json"

    with open(inputs_path,'r') as inps:

        inputs = json.load(inps)

        SIM = Simulator(inputs)

