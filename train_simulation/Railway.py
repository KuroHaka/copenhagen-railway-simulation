import json
from .Entity import Entity

class Station(Entity):
    image = "path"

    def __init__(self, name, x, y, passengers):
        self.name = name
        self.x = x
        self.y = y
        self.passengers = passengers

    def add_passengers(self, num):
        self.passengers += num
    
    def sub_passengers(self, num):
        self.passengers -= num

    @staticmethod
    def from_json(json_dct):
      return Station(json_dct["name"],
                    json_dct["X"],
                    json_dct["Y"],
                   0)


class Connection(Entity):
    image = ""
    def __init__(self, station_start, station_end, distance):
        self.station_start = Station(station_start,0,0,0)
        self.station_end = Station(station_end,0,0,0)
        self.distance = distance*1000

    @classmethod
    def from_json(self, json_dct):
        return Connection(json_dct['station A'],
                   json_dct['station B'],
                   json_dct['distance'])
