from others.simulation_skeleton import Person
from datetime import datetime


class Person:
    def __init__(self, start_station, destination, traffic_load):
        self.start_station = start_station
        self.destination = destination
        self.traffic_load = traffic_load
        self.status = 'ready'
        self.start_time = datetime.now()
        self.end_time = None
        self.travel_time = None

    def start_ride(self):
        self.status = 'on board'

    def end_ride(self):
        self.status = 'done'
        self.end_time = datetime.now()
        self.travel_time = self.ride_duration()
        #TODO cal method to register ride
        self.delete_person()

    def delete_person(self):
        del self

    def ride_duration(self):
        return self.end_time -self.start_time
