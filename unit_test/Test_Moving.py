import unittest
import os, sys, json
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Moving import Moving, Train, Carrier
from train_simulation.Simulation import Simulation
from train_simulation.Passenger import Passenger
from datetime import datetime


class Test_moving(unittest.TestCase):
    def test_move_to_over_capacity(self):
        sim = Simulation()
        sim.trains['0']
        train = sim.trains['0']
        passengers = []
        for i in range(750):
            passengers.append(Passenger('Hillerød','kbh h',datetime.now()))

        Stations['Hillerød'].add_passengers(passengers)
        train.boardPassengers(Stations['Hillerød'])
        self.assertTrue(
            len(train._passengers) == 700 and len(Stations['Hillerød'].get_passengers()) == 50
        )
    def test_move_to(self):
        sim = Simulation()
        sim.trains['0']
        train = sim.trains['0']
        passengers = []
        for i in range(699):
            passengers.append(Passenger('Hillerød','kbh h',datetime.now()))

        Stations['Hillerød'].add_passengers(passengers)
        train.boardPassengers(Stations['Hillerød'])
        self.assertTrue(
            len(train._passengers) == 699 and len(Stations['Hillerød'].get_passengers()) == 0
        )    
    def test_accelerate(self):
        sim = Simulation()
        sim.trains['0']
        train = sim.trains['0']
        train._accelerateTo = 100
        train.accelerate(1)
        self.assertTrue(train._speed == 1.3)   
    def test_decelerate(self):
        sim = Simulation()
        sim.trains['0']
        train = sim.trains['0']
        train._speed = 100
        train.decelerate(1)
        self.assertTrue(train._speed == 98.8) 
        

if __name__ == "__main__":
    unittest.main()