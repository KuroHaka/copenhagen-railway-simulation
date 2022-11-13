import json

Stations = {}
Connections = {}

class Station():
    __passengers = []

    def __init__(self, name:str, x, y, passengers:int, idle_time, lines:[str], is_last_station:bool):
        self.name = name
        self.x = x
        self.y = y
        self.__idle_time = idle_time
        self.__lines = lines
        self.__is_last_station = is_last_station
        Stations[name] = self

    #for info printing
    # def __str__(self):
    #     return f"""
    #         "name": {self.name},
    #         "x": {self.x},
    #         "y": {self.y},
    #         "idle_time": {self.get_idle_time()},
    #         "passengers": {self.get_passengers()},
    #         "is_last_station": {self.is_last_station()},
    #         "lines": {self.get_lines()}"""

    def get_passengers(self)->int:
        return self.__passengers

    def get_lines(self)->list:
        return self.__lines

    def is_last_station(self)->bool:
        return self.__is_last_station

    def get_idle_time(self)->int:
        return self.__passengers

    def add_passengers(self, passengers):
        for passenger in passengers:
            self.__passengers.append(passenger)
    
    def sub_passengers(self, passengers):
        for passenger in passengers:
            self.__passengers.remove(passenger)

    def add_passenger(self,passenger):
        self.__passengers.append(passenger)

    def sub_passenger(self,passenger):
        self.__passengers.remove(passenger)


    def name(self):
        return self.name

    @staticmethod
    def from_json(json_dct):
        Station(json_dct["name"],
                    json_dct["x"],
                    json_dct["y"],
                    json_dct["passengers"],
                    json_dct["idle_time"],
                    json_dct["lines"],
                    json_dct["is_last_station"])


class Connection():
    def __init__(self, station_start, station_end, distance):
        self.station_start = Stations[station_start]
        self.station_end = Stations[station_end]
        self.distance = distance*1000
        Connections[(station_start, station_end)] = self
    
    # for info printing
    def __str__(self):
        return f"""
            "station_start": {self.station_start.name},
            "station_end": {self.station_start.name},
            "distance": {self.distance}"""

    @classmethod
    def from_json(self, json_dct):
        Connection(json_dct['station A'],
                   json_dct['station B'],
                   json_dct['distance'])
        #Connection(json_dct['station B'],
                   #json_dct['station A'],
                   #json_dct['distance'])
        
        
