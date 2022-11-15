# from others.simulation_skeleton import Person
import json
from datetime import datetime
import random
# from Railway import Station


class Person:
    def __init__(self, start_station, destination, time):  # I think that start station wil be good for us to generate report- can deleted if you are not agree
        self.start_station = start_station
        self.destination = destination
        self.status = 'ready'
        self.time = time
        self.end_time = None
        self.travel_time = None

    def start_ride(self):
        self.status = 'on board'

    def end_ride(self):
        self.status = 'done'
        self.end_time = datetime.now()
        self.travel_time = self.ride_duration()
        # TODO cal method to register ride in a report
        self.delete_person()

    def delete_person(self):
        del self

    def ride_duration(self):
        return self.end_time - self.time

    @staticmethod
    def create_passengers(critical_stations, time, n_passengers):
        stations_json = json.load(open('../assets/stations.json', mode="r", encoding="utf-8"))
        stations = list(stations_json.keys())
        critical_stations_weight = 2  # 50% of the passengers will be directed to critical stations (perhaps  set it at the constructor?)
        critical_stations_passengers = n_passengers // critical_stations_weight
        passengers_list = {'passengers': []}

        for passenger in range(critical_stations_passengers):  # generate passengers only to creitical stations
            destination = random.choice(critical_stations)
            passengers_list['passengers'].append(Person('start_station', destination, time))
        for passenger in range(n_passengers - critical_stations_passengers):  # generate passengers for all stations
            destination = random.choice(stations)
            passengers_list['passengers'].append(Person('start_station', destination, time))

        return passengers_list
