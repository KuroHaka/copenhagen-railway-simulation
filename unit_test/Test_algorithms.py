import unittest
import os, sys, json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Algorithms import Algorithms
from train_simulation.Railway import Station, Connection, Stations, Connections, Lines
from train_simulation.Moving import Moving, Train, Carrier
from train_simulation.Simulation import Simulation
from train_simulation.Passenger import Passenger
from datetime import datetime



class Test_algorithms(unittest.TestCase):
    def test_get_path(self):
        stations_file = open(
            os.path.join(dirname, "../assets/new_stations.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(stations_file, object_hook=Station.from_json)

        new_connections_file = open(
            os.path.join(dirname, "../assets/new_connections.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(new_connections_file, object_hook=Connection.from_json)

        algo = Algorithms(Connections, Stations, Lines)
        self.assertEqual(
            algo.get_path("Lyngby", "Malmparken").nodes,
            [
                "Lyngby",
                "Jærgersborg",
                "Gentofte",
                "Bernstorffsvej",
                "Hellerup",
                "Ryparken",
                "Bispebjerg",
                "Nørrebro",
                "Fuglebakken",
                "Grøndal",
                "Flintholm",
                "Vanløse",
                "Jyllingevej",
                "Islev",
                "Husum",
                "Herlev",
                "Skovlunde",
                "Malmparken",
            ],
        )
        self.assertEqual(
            algo.get_path("Bispebjerg", "Hillerød").nodes,
            [
                "Bispebjerg",
                "Ryparken",
                "Hellerup",
                "Bernstorffsvej",
                "Gentofte",
                "Jærgersborg",
                "Lyngby",
                "Sorgenfri",
                "Virum",
                "Holte",
                "Birkerød",
                "Allerød",
                "Hillerød",
            ],
        )

    def test_get_path_trains(self):
        stations_file = open(
            os.path.join(dirname, "../assets/new_stations.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(stations_file, object_hook=Station.from_json)

        new_connections_file = open(
            os.path.join(dirname, "../assets/new_connections.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(new_connections_file, object_hook=Connection.from_json)

        algo = Algorithms(Connections, Stations, Lines)
        self.assertEqual(
            algo.get_path_trains("Lyngby", "Malmparken"),
            [
                {
                    "line": "a",
                    "path": [
                        "Lyngby",
                        "Jærgersborg",
                        "Gentofte",
                        "Bernstorffsvej",
                        "Hellerup",
                    ],
                },
                {
                    "line": "f",
                    "path": [
                        "Hellerup",
                        "Ryparken",
                        "Bispebjerg",
                        "Nørrebro",
                        "Fuglebakken",
                        "Grøndal",
                        "Flintholm",
                    ],
                },
                {
                    "line": "c",
                    "path": [
                        "Flintholm",
                        "Vanløse",
                        "Jyllingevej",
                        "Islev",
                        "Husum",
                        "Herlev",
                        "Skovlunde",
                        "Malmparken",
                    ],
                },
            ],
        )
        self.assertEqual(
            algo.get_path_trains("Bispebjerg", "Hillerød"),
            [
                {"line": "f", "path": ["Bispebjerg", "Ryparken", "Hellerup"]},
                {
                    "line": "a",
                    "path": [
                        "Hellerup",
                        "Bernstorffsvej",
                        "Gentofte",
                        "Jærgersborg",
                        "Lyngby",
                        "Sorgenfri",
                        "Virum",
                        "Holte",
                        "Birkerød",
                        "Allerød",
                        "Hillerød",
                    ],
                },
            ],
        )


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
