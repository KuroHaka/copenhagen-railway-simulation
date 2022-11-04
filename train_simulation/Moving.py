from Entity import Entity
from abc import abstractproperty
import json

""" README:

    Removed the abstract property from Moving and Entity

    TRAIN:
        Acceleration and deacceleration function uses sleep, so not to instantly 
        accelerate to min/max speed. This needs to be changed to follow some sort
        of tick

        All functions return their related value, makes it easier for testing
        purposes

        #TODO: 
            Trains knowledge of how far along the route to a station it is
            Passengers being passengers instead of numbers

    CARRIER:


"""


class Moving(Entity):
    def position_x(self):
        pass

    def position_y(self):
        pass

    def display_element(self):
        self.image

class Carrier(Moving):
    pass

class Train(Moving):
    #Amount of passengers on train
    _passengers = 0

    #Speed of train
    _speed = 0

    #Max speed of train
    _maxSpeed = 120

    #Acceleration of train
    _acceleration = 1.3
    _decceleration = 1.2

    #0 when not at a station otherwise station
    _atStation = 0

    #Is the train moving
    _moving = False

    #0 when at a station otherwise station
    _movingTo = 0
    _movingFrom = 0

    #Initialisation of the train
    def __init__(self, atStation, moveTo):
        self._atStation = atStation
        self._movingTo = moveTo

    def loadFromJSON(json):
        return Train(json['moveFrom'],json['moveTo'])

    def defineMOVE(self, move):
        self._moveEntity = move
        
    def atStation(self):
        return self._atStation

    def moving(self):
        return self._moving

    def arriveAt(self,station):
        self._atStation = station
        self._moving = False
        return self._atStation
    
    def moveTo(self,station):
        self._movingFrom = self._atStation
        self._movingTo = station
        self._atStation = 0
        self._moving = True
        self.accelerate()
        return self._movingTo

    def goingFromTo(self):
        return (self._movingFrom,self._movingTo)

    def passengerNumber(self):
        return self._passengers

    def boardPassengers(self,passengers):
        self._passengers += passengers
        return self._passengers

    def disembarkPassengers(self,passengers):
        self._passengers -= passengers
        return self._passengers

    def availablePassengerSpace(self):
        return 700 - self._passengers

    def maxPassengers(self):
        return 700

    def speed(self):
        return self._speed

    def accelerate(self):
        while self._speed < 120:
            self._speed = self._speed + self._acceleration
            #sleep(0.1)
        return self._speed

    def decelerate(self):
        while self._speed > 1:
            self._speed = self._speed - self._decceleration
            #sleep(0.1)
        self._speed = 0
        return self._speed

    def printInformation(self):
        print(f"passengers: {self._passengers}")
        print(f"speed: {self._speed}")
        print(f"atStation: {self._atStation}")
        print(f"moving: {self._moving}")
        print(f"movingTo: {self._movingTo}")
        print(f"movingFrom: {self._movingFrom}")
        print(f"availablePassengerSpace: {self.availablePassengerSpace()}")


# train = json.loads('[{"moveFrom": "station_a","moveTo": "station_b"}]', object_hook=Train.loadFromJSON)
# train[0].printInformation()
# print()
# train[0].boardPassengers(350)
# train[0].disembarkPassengers(50)
# train[0].moveTo('Nørreport')
# train[0].printInformation()
# train[0].decelerate()
# train[0].arriveAt('Nørreport')
# print()
# train[0].printInformation()