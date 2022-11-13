from Person import Person
from datetime import datetime
import datetime
import time
import random


class Passengers_generator:
    passengers = {}

    def __init__(self, low_load, mid_load, high_load, interval, current_load, station):
        self.low_load = low_load
        self.mid_load = mid_load
        self.high_load = high_load
        self.interval = interval
        self.current_load = current_load
        self.station = station
        self.status = 'stop'
        self.passengers = {}
    def generate_passengers(self):
        self.status = 'run'
        start_time = datetime.datetime.now()
        end_of_interval = datetime.timedelta(seconds=self.interval)
        count = 0
        print(len(self.passengers))
        while datetime.datetime.now() < start_time + end_of_interval:
            match self.current_load:
                case "low":
                    max_per_interval = self.low_load
                case "mid":
                    max_per_interval = self.mid_load
                case "high":
                    max_per_interval = self.high_load
            if (count < max_per_interval):
                for person in range(0, max_per_interval // 10):
                    name = 'passenger_{}'.format(time.time())
                    self.passengers[name] = Person(self.station, self.generate_destination(), self.current_load)
                    count = count + 1
                time.sleep(self.interval / 10)
        self.status = 'stop'
        self.re_generate_passengers()

    def re_generate_passengers(self):
        if (self.status == 'stop'):
            self.generate_passengers()

    def generate_destination(self):
        # TODO - find how we are generating the stations and build a method to extract all stations names (except the current one)
        temp_station_list = ["Valby", "Kbh H", "Carlsberg", "Sydhavn", "Sajlor", "KB haleln", "Kastrup", "Lufthavn"]

        return random.choice(temp_station_list)
