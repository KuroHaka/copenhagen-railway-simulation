import unittest, datetime
import os, sys, json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Railway import Stations
from train_simulation.Simulation import CarrierSimulation


class Test_Simulation(unittest.TestCase):
    def test_loadbalancer(self):
        sim = CarrierSimulation(0, [], datetime.datetime.now())
        time = 0
        sim.loadbalanceGenerator(time)
        print((sim.stations["Køge"].carriers))
        print((Stations["Køge"].carriers))
        print((sim.carriers))
        pass


if __name__ == "__main__":
    unittest.main()