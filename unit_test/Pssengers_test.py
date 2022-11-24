import unittest
import json, os, sys
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from train_simulation.Person import Person

class TestPassenger(unittest.TestCase):
    def test_create_person(self):
        p = Person('start_station', 'destination', datetime.now(),1)
        self.assertEqual(p.start_station, 'start_station')
        self.assertEqual(p.destination, 'destination')
        self.assertEqual(p.status, 'ready')
        self.assertEqual(p.end_time, None)
        self.assertEqual(p.travel_time, None)
        self.assertEqual(p.time.strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))

    def test_start_ride(self):

        p = Person('start_station', 'destination', datetime.now(),1)

        p.start_ride()
        self.assertEqual(p.status, 'on board')
        self.assertEqual(p.end_time, None)
        self.assertEqual(p.travel_time, None)


    def test_end_ride(self):
         p = Person('start_station', 'destination', datetime.now(),1)
         p.start_ride()
         p.end_ride()
         self.assertEqual(p.status, 'done')
         self.assertEqual(p.end_time.strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'))
         self.assertTrue(p.travel_time < timedelta(minutes=1))

    def test_create_passengers(self):
        critical_stations =["Hillerød","Lyngby","Gentofte","Køge","Herlev"]
        today =  datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        time={'start': today,'end':tomorrow}
        ps =Person.create_passengers(critical_stations,time,100)
        self.assertEqual(len(ps['passengers']), 100)

    def test_create_json_file(self):
        with open(os.path.join(dirname, '../assets/passengers.json'),  encoding="utf-8") as json_file:
            data = json.load(json_file)

            for element in data: # delete all file content to make sure it is an empty file
                del element
        critical_stations = ["Hillerød", "Lyngby", "Gentofte", "Køge", "Herlev"]
        today = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        time = {'start': today, 'end': tomorrow}
        Person.create_passengers(critical_stations, time, 100)
        with open(os.path.join(dirname, '../assets/passengers.json'),  encoding="utf-8") as json_file:
            data = json.load(json_file)
        self.assertEqual(len(data), 100)


if __name__ == '__main__':
    unittest.main()