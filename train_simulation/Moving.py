from Entity import Entity
from abc import abstractproperty
import json

""" README:

    Removed the abstract property from Moving and Entity

    TRAIN:
        #TODO: 
            Passengers being passengers instead of numbers

    CARRIER:


"""


class Moving(Entity):

    @abstractproperty
    def image(self):
        pass

    def position_x(self):
        pass

    def position_y(self):
        pass

    def display_element(self):
        self.image

class Carrier(Moving):
    pass

class Train(Moving):
    image = ""

    #Trains identifier:
    _uid = 0

    #Which line the train is running
    _line = 0

    #Amount of passengers on train
    _passengers = 0

    #Speed of train
    _speed = 0
    

    #Max speed of train in m/s
    _maxSpeed = 33.33
    
    #Max speed the train can go before it needs to decelerate again
    _accelerateTo = 0

    #Acceleration of train
    _acceleration = 1.3
    _deceleration = 1.2

    #0 when not at a station otherwise station
    _atStation = 0
    _cameFrom = 0

    #Set to 180 (seconds)
    _remainingWaitingTime = 0

    #Is the train moving
    _moving = False
    
    #Is the train decelerating
    _decelerating = False

    #0 when at a station otherwise station
    _movingTo = 0
    _movingFrom = 0

    #Different distances
    _distanceToStation = 0
    _distanceMovedTowardsStation = 0
    _distanceFromStationToDecelerate = 0
    

    #Initialisation of the train
    def __init__(self, uid, atStation, moveTo):
        self._uid = uid
        self._atStation = atStation
        self._movingTo = moveTo

    def loadFromJSON(json):
        return Train(json['uid'],json['atStation'],json['moveTo'])


    #If the station is close, the train can only accelerate so much
    def calculateAccelerateTo(self, distance):
        distAcc = 0
        distDeacc = 0

        for i in range(29):
            distAcc += 1.3*i
            distDeacc += 1.2*i
            if distAcc + distDeacc >= distance:
                self._distanceFromStationToDecelerate = distDeacc
                return 1.3*i
        self._distanceFromStationToDecelerate = distDeacc
        return self._maxSpeed

    #Functions for when atStation
    def moveTo(self,station,distance,time):

        #wait
        if self._remainingWaitingTime > 0:
            time = self.wait(time)
            if time == 0:
                return 0

        self._movingFrom = self._atStation
        self._movingTo = station
        self._atStation = 0
        self._cameFrom = 0
        self._distanceToStation = distance
        self._moving = True

        self._accelerateTo = self.calculateAccelerateTo(distance)
        time = self.accelerate(time)
        return time

    def accelerate(self, time):
        while self._speed < self._maxSpeed and self._speed < self._accelerateTo and 0 < time:
            self._speed = self._speed + self._acceleration
            if self._speed > self._maxSpeed:
                self._speed = self._maxSpeed
            self._distanceMovedTowardsStation += self._speed
            time -= 1
        return time

    def wait(self,time):
        if time <= self._remainingWaitingTime:
            self._remainingWaitingTime -= time
            return 0
        else:
            time -= self._remainingWaitingTime
            self._remainingWaitingTime = 0
            return time

    def boardPassengers(self, passengers):
        self._passengers += passengers
        return self._passengers

    def disembarkPassengers(self, passengers):
        self._passengers -= passengers
        return self._passengers

    #Return a tuple consisting of the station the train came from and the station the train is at
    def cameFromAtStation(self):
        return (self._cameFrom,self._atStation)
    
    #
    #Functions for when moving:
    #

    #arrive at a station
    def arriveAt(self, station, time):
        self._atStation = station
        self._cameFrom = self._movingFrom
        self._movingTo = 0
        self._movingFrom = 0
        self._distanceToStation = 0
        self._distanceMovedTowardsStation = 0
        self._distanceFromStationToDecelerate = 0
        self._remainingWaitingTime = 180
        self._moving = False
        time = self.wait(time)
        return time

    #Keep moving alon the track towards the next station
    def keepMoving(self, time):
        if (self._speed < self._maxSpeed and not self._decelerating):
            time = self.accelerate(time)

        if (self._decelerating):
            time = self.decelerate(time)
            if self._speed == 0:
                time = self.arriveAt(self._movingTo, time)
            return time

        if (self._distanceMovedTowardsStation + time * self._speed < self._distanceToStation - self._distanceFromStationToDecelerate):
            self._distanceMovedTowardsStation += time * self._speed
            return 0
        
        for i in range(time):
            if (self._distanceMovedTowardsStation + i * self._speed >= self._distanceToStation - self._distanceFromStationToDecelerate):
                self._distanceMovedTowardsStation += i * self._speed
                time -= i
                break

        self._decelerating = True
        time = self.decelerate(time)
        if self._speed == 0:
            time = self.arriveAt(self._movingTo,time)
        return time

    def decelerate(self,time):
        while self._speed > 0 and 0 < time:
            self._speed = self._speed - self._deceleration
            if self._speed <= 0:
                self._speed = 0
                self._decelerating = False
            self._distanceMovedTowardsStation += self._speed
            time -= 1
        return time

    
    #Tuple returning the station is moving away from, and the station it is moving towards
    def goingFromTo(self):
        return (self._movingFrom,self._movingTo)

    # Train does not yet have a line
    def getLine(self):
        return self._line

    

    #Other getters and functions
    def moving(self):
        return self._moving

    def passengerNumber(self):
        return self._passengers

    def availablePassengerSpace(self):
        return 700 - self._passengers

    def maxPassengers(self):
        return 700

    def printInformation(self):
        print(f"uid: {self._uid}")
        print(f"speed: {self._speed}")
        print(f"atStation: {self._atStation}")
        print(f"remainingWaitingTime {self._remainingWaitingTime}")
        print(f"cameFrom: {self._cameFrom}")
        print(f"moving: {self._moving}")
        print(f"movingTo: {self._movingTo}")
        print(f"movingFrom: {self._movingFrom}")
        print(f"distanceMovedTowardsStation: {self._distanceMovedTowardsStation}")
        print(f"distanceFromStationToDecelerate: {self._distanceFromStationToDecelerate}")
        print(f"passengers: {self._passengers}")
        print(f"availablePassengerSpace: {self.availablePassengerSpace()}")

    def getUID(self):
        return self._uid


#train = json.loads('[{"uid": "0", "atStation": "station_a","moveTo": "station_b"}]', object_hook=Train.loadFromJSON)
#print(train[0].calculateAccelerateTo(100))
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