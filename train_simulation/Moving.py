from .Entity import Entity
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
    _passengers = []
    _maxPassengers = 700

    #Speed of train
    _speed = 0
    

    #Max speed of train in m/s
    _maxSpeed = 33.33
    
    #Max speed the train can go before it needs to decelerate again (if the distance to next station is small)
    _accelerateTo = 0

    #Acceleration of train
    _acceleration = 1.3
    _deceleration = 1.2

    #0 when not at a station otherwise Station
    _atStation = 0
    _cameFrom = 0

    #Amount if seconds to wait at a station. Set to 180 seconds
    _remainingWaitingTime = 0

    #Is the train moving
    _moving = False

    #If a moving train should stop
    _shouldStop = False
    
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

        for i in range(28):
            distAcc += 1.3*i
            distDeacc += 1.2*i
            if distAcc + distDeacc >= distance:
                self._distanceFromStationToDecelerate = distDeacc
                return 1.3*i
        self._distanceFromStationToDecelerate = distDeacc
        return self._maxSpeed

    #Functions for when atStation
    def moveTo(self,station,distance,time,trainOnTracks):

        if self._shouldStop:
            return 0

        #wait
        if self._remainingWaitingTime > 0:
            time = self.wait(time)
            if time == 0:
                return 0

        if trainOnTracks:
            print(f"Train {self._uid} is not moving to {station.name} because there is a train on the tracks")
            return 0
        
        self.boardPassengers(self._atStation)
        
        self._movingFrom = self._atStation
        self._movingTo = station
        self._atStation = 0
        self._cameFrom = 0
        self._distanceToStation = distance
        self._moving = True

        self._accelerateTo = self.calculateAccelerateTo(distance)
        time = self.accelerate(time)
        return time

    #For when train is at the end of a line
    def turnAround(self):
        return (self._cameFrom,self._distanceToStation)

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

    def boardPassengers(self, station):
        #print(f"Boarding passengers for train {self._uid}: amount of passengers that can board: {station.passengers}, available passenger space: {self.availablePassengerSpace()}")
        
        if len(station.get_passengers()) < self.availablePassengerSpace():
            for passenger in station.get_passengers():
                #print(passenger,station.name)
                self._passengers.append(passenger)
                station.sub_passenger(passenger)

        else:
            passengerAmount = self.availablePassengerSpace()
            for i,passenger in enumerate(station.get_passengers()):
                if i >= passengerAmount:
                    break
                self._passengers.append(passenger)
                station.sub_passenger(passenger)
                
    

    def disembarkPassengers(self, station):
        for passenger in self._passengers:
            if passenger._destination == station.name:
                self._passengers.remove(passenger)
                passenger.isArrived()
        #Should account for Station space

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
        self._distanceMovedTowardsStation = 0
        self._distanceFromStationToDecelerate = 0
        self._remainingWaitingTime = 180
        self._moving = False

        self.disembarkPassengers(station)

        time = self.wait(time)
        return time

    #Keep moving alon the track towards the next station
    def keepMoving(self, time):
        if self._shouldStop:
            self.decelerate(time)
            return 0

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

    #Signal that the train should stop
    def signalStop(self):
        self._shouldStop = True
        

    #Signal that the train should start up again
    def signalStart(self):
        self._shouldStop = False
    
    #Tuple returning the station is moving away from, and the station it is moving towards
    def goingFromTo(self):
        return (self._movingFrom,self._movingTo)

    
    # Train does not yet have a line
    def getLine(self):
        return self._line

    
    #Other getters and functions
    def moving(self):
        return self._moving

    def availablePassengerSpace(self):
        return self._maxPassengers - len(self._passengers)

    def printInformation(self):
        print(f"uid: {self._uid}")
        print(f"speed: {self._speed}")
        
        if not self._atStation:
            print(f"atStation: {self._atStation}")
        else:
            print(f"atStation: {self._atStation.name}")
        print(f"remainingWaitingTime {self._remainingWaitingTime}")
        
        if not self._cameFrom:
            print(f"cameFrom: {self._cameFrom}")
        else:
            print(f"cameFrom: {self._cameFrom.name}")

        print(f"moving: {self._moving}")

        if not self._movingTo:
            print(f"movingTo: {self._movingTo}")
        else:
            print(f"movingTo: {self._movingTo.name}")
        
        
        if not self._movingFrom:
            print(f"movingFrom: {self._movingFrom}")
        else:
            print(f"movingFrom: {self._movingFrom.name}")

        print(f"distanceToStation: {self._distanceToStation}")
        print(f"distanceMovedTowardsStation: {self._distanceMovedTowardsStation}")
        print(f"distanceFromStationToDecelerate: {self._distanceFromStationToDecelerate}")
        #print(f"passengers: {len(self._passengers)}")
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