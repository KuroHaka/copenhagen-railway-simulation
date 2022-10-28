import json

class Station:

    def __init__(self, name, x, y, passengers):
        self.name = name
        self.passengers = passengers

    def __iter__(self):
        yield from {
            "name": self.name,
            "passengers": self.passengers
        }.items()

    def add_passengers(self, num):
        self.passengers += num
    
    def sub_passengers(self, num):
        self.passengers -= num

    @staticmethod
    def from_json(json_dct):
      return Station(json_dct['name'],
                   json_dct['passengers'])


json_str = '[{"name": "station_a", "x": 10, "y": 20, "passengers": 10}, {"name": "station_b", "x": 10, "y": 40, "passengers": 30}]'
trains = json.loads(json_str, object_hook=Station.from_json)
print(trains[0].passengers)


