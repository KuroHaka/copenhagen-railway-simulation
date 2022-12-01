# from others.simulation_skeleton import Person
import json, os, sys, uuid, calendar

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Railway import Station

from datetime import datetime, timedelta
import random


# from Railway import Station


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

@staticmethod
def create_passengers(critical_stations, time, n_passengers):
    new_stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8")
    stations_json = json.load(new_stations_file)
    stations = [x["name"] for x in stations_json]
    critical_stations_weight = 0.25  # 25% of the passengers will be directed to critical stations (perhaps  set it at the constructor?)
    critical_stations_passengers = int(n_passengers * critical_stations_weight)
    passengers_list = {'passengers': []}
    i = 0

    for passenger in range(critical_stations_passengers):  # generate passengers only to creitical stations
        start_station = random.choice(critical_stations)
        destination = random.choice(stations)
        while destination == start_station:
            destination = random.choice(stations)
        travel_time = str(random_date(time['start'], time['end']))
        passengers_list['passengers'].append(Person(start_station, destination, travel_time,i))
        i += 1
    
    for passenger in range(n_passengers - critical_stations_passengers):  # generate passengers for all stations
        start_station = random.choice(stations)
        destination = random.choice(stations)
        while destination == start_station:
            destination = random.choice(stations)
        travel_time = str(random_date(time['start'], time['end']))
        passengers_list['passengers'].append(Person(start_station, destination, travel_time,i))
        i += 1

        json_string = json.dumps([ob.__dict__ for ob in passengers_list['passengers']], indent=4,ensure_ascii=False)
        with open(os.path.join(dirname, '../assets/passengers.json'), mode="w", encoding="utf-8") as outfile:
            outfile.write(json_string)
    return passengers_list


class Person:
    def __init__(self, start_station, destination, start_time, id):  # I think that start station wil be good for us to generate report- can deleted if you are not agree
        self.start_station = start_station
        self.destination = destination
        self.isArrived = False
        self.start_time = start_time
        self.end_time = None
        self.travel_time = None
        self.id = id
        self.path = []
        self.remainingPath = []
        self.intermediateDestination = ""
        self.atStation = ""
        

    def setPath(self,path):
        self.path = path
        self.remainingPath = path[:]
        self.intermediateDestination = self.remainingPath[0]["path"][-1]

    def updatePath(self, arriveTime, station):
        if self.destination == self.intermediateDestination:
            self.arrived(arriveTime)
        else:
            self.remainingPath.pop(0)
            self.intermediateDestination = self.remainingPath[0]["path"][-1]
            station.add_passenger(self)

    def arrived(self, arriveTime):
        self.isArrived = True
        self.end_time = arriveTime
        self.travel_time = (self.end_time - self.start_time)

    def isArrived(self):
        return self.isArrived
    
    def delete_person(self):
        del self

    def ride_duration(self):
        return self.end_time - self.time

    def getdestination(self):
        return self.destination

    def getid(self):
        return self.id

    def getTravelTime(self):
        return self.travel_time