from .Entity import Entity
from abc import abstractproperty
import json, datetime

""" README:

    Removed the abstract property from Moving and Entity

    CARRIER:


"""

class Train():

    #Global static variables
    image = ""
    
    #Max amount of passengers on train
    _maxPassengers = 700

    #Max speed of train in m/s
    _maxSpeed = 33.33
    
    #Acceleration of train
    _acceleration = 1.3
    _deceleration = 1.2

    #Initialisation of the train
    def __init__(self, uid, atStation, moveTo, line, start_time):
        #Trains identifier:
        self._uid = uid
        
        #On which line the train is running
        self._line = line

        #Passengers on the train
        self._passengers = []

        #Speed of train
        self._speed = 0

        #Max speed the train can go before it needs to decelerate again (if the distance to next station is small)
        self._accelerateTo = 0

        #0 when not at a station otherwise Station
        self._atStation = atStation
        self._cameFrom = 0
        
        #Amount if seconds to wait at a station. Set to 180 seconds
        self._remainingWaitingTime = 0

        #Is the train moving
        self._moving = False

        #If a moving train should stop
        self._shouldStop = False
        
        #Is the train decelerating
        self._decelerating = False

        #0 when at a station otherwise station
        self._movingTo = moveTo
        self._movingFrom = 0

        #Different distances
        self._distanceToStation = 0
        self._distanceMovedTowardsStation = 0
        self._distanceFromStationToDecelerate = 0

        #When the simulation began
        self.start_time = start_time


       

    def loadFromJSON(json):
        return Train(json['uid'],json['atStation'],json['moveTo'],json['line'])


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
            #print(f"Train {self._uid} of line {self._line} is not moving to {station.name} because there is a train on the tracks")
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
        passengers_to_remove = []
        if len(station.get_passengers()) < self.availablePassengerSpace():
            for passenger in station.get_passengers():
                if self._line in passenger.remainingPath[0]["line"]:
                    self._passengers.append(passenger)
                    passengers_to_remove.append(passenger)
        else:
            passengerAmount = self.availablePassengerSpace()
            for i,passenger in enumerate(station.get_passengers()):
                if i > passengerAmount:
                    break
                if self._line in passenger.remainingPath[0]["line"]:
                    self._passengers.append(passenger)
                    passengers_to_remove.append(passenger)

        station.sub_passengers(passengers_to_remove)

    #Should account for Station space?
    def disembarkPassengers(self, station, totalTime):
        for passenger in self._passengers:
            if passenger.intermediateDestination == station.name:
                self._passengers.remove(passenger)
                passenger.atStation = station.name
                passenger.updatePath((self.start_time + datetime.timedelta(seconds=totalTime)), station)
        

    #Return a tuple consisting of the station the train came from and the station the train is at
    def cameFromAtStation(self):
        return (self._cameFrom,self._atStation)
    
    #
    #Functions for when moving:
    #

    #arrive at a station
    def arriveAt(self, station, time, totalTime):
        self._atStation = station
        self._cameFrom = self._movingFrom
        self._movingTo = 0
        self._movingFrom = 0
        self._distanceMovedTowardsStation = 0
        self._distanceFromStationToDecelerate = 0
        self._remainingWaitingTime = 60
        self._moving = False

        # if self._line == 'f-line' and self._uid == '7':
        #     print(f"Train: {self._uid} arrived at station: {self._atStation.name} after running for {(totalTime-time)/60} minutes")

        self.disembarkPassengers(station,totalTime)

        time = self.wait(time)
        return time

    #Keep moving alon the track towards the next station
    def keepMoving(self, time, totalTime):
        if self._shouldStop:
            self.decelerate(time)
            return 0

        if (self._speed < self._maxSpeed and not self._decelerating):
            time = self.accelerate(time)

        if (self._decelerating):
            time = self.decelerate(time)
            if self._speed == 0:
                time = self.arriveAt(self._movingTo, time, totalTime)
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
            time = self.arriveAt(self._movingTo,time, totalTime)
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
        print(f"passengers: {len(self._passengers)}")
        print(f"availablePassengerSpace: {self.availablePassengerSpace()}")

    def getUID(self):
        return self._uid


class Carrier():
    #Global static variables
    image = ""
    
    #Max amount of passengers on Carrier
    _maxPassengers = 5

    #Max speed of Carrier in m/s
    _maxSpeed = 33.33
    
    #Acceleration of carrier
    _acceleration = 1.5
    _deceleration = 1.4

    #Initialisation of the carrier
    def __init__(self, uid, atStation, start_time):
        #carriers identifier:
        self._uid = uid

        #Passengers on the carrier
        self._passengers = []

        #Speed of carrier
        self._speed = 0

        #Path the train should take
        self._path = []
        self._destination = 0

        #Max speed the carrier can go before it needs to decelerate again (if the distance to next station is small)
        self._accelerateTo = 0

        #0 when not at a station otherwise Station
        self._atStation = atStation
        self._cameFrom = 0

        #Is the carrier moving
        self._moving = False

        #If a moving carrier should stop
        self._shouldStop = False
        
        #Is the carrier decelerating
        self._decelerating = False

        #0 when at a station otherwise station
        self._movingTo = 0
        self._movingFrom = 0

        #Different distances
        self._distanceToStation = 0
        self._distanceMovedTowardsStation = 0
        self._distanceFromStationToDecelerate = 0

        self.start_time = start_time
        self.empty = False


    #If the station is close, the train can only accelerate so much
    def calculateAccelerateTo(self, distance):
        distAcc = 0
        distDeacc = 0

        for i in range(28):
            distAcc += self._acceleration*i
            distDeacc += self._deceleration*i
            if distAcc + distDeacc >= distance:
                self._distanceFromStationToDecelerate = distDeacc
                return self._acceleration*i
        self._distanceFromStationToDecelerate = distDeacc
        return self._maxSpeed

    #Functions for when atStation
    def moveTo(self,destination,time,algo,connections, empty):
        if self._shouldStop:
            return 0

        if empty:
            self.empty = True

        self._path = algo.get_path(self._atStation.name,destination.name).nodes
        self._destination = destination
        
        self._movingFrom = self._atStation.name
        self._path.pop(0)
        self._movingTo = self._path.pop(0)

        if (self._movingFrom,self._movingTo) in connections:
            self._distanceToStation = connections[(self._movingFrom,self._movingTo)].distance
        else:
            print(f"Carrier {self._uid} is fucked, connection does not exist")

        self._atStation.sub_carrier(self)
        self._atStation = 0
        self._cameFrom = 0
        self._moving = True

        self._accelerateTo = self.calculateAccelerateTo(self._distanceToStation)
        

        return self.accelerate(time)

    def accelerate(self, time):
        while self._speed < self._maxSpeed and self._speed < self._accelerateTo and 0 < time:
            self._speed = self._speed + self._acceleration
            if self._speed > self._maxSpeed:
                self._speed = self._maxSpeed
            self._distanceMovedTowardsStation += self._speed
            time -= 1
        return time

    def boardPassengers(self, station, destination):
        #print(f"Boarding passengers for train {self._uid}: amount of passengers that can board: {station.passengers}, available passenger space: {self.availablePassengerSpace()}")
        passengersToRemove = []
        for passenger in station.get_passengers():
            if passenger.destination == destination:
                self._passengers.append(passenger)
                passengersToRemove.append(passenger)
                if not self.availablePassengerSpace():
                    break
        station.sub_passengers(passengersToRemove)


                
    
    #Should account for Station space?
    def disembarkPassengers(self, station, totalTime):
        for passenger in self._passengers:
            self._passengers.remove(passenger)
            passenger.arrived((self.start_time + datetime.timedelta(seconds=totalTime)))
        
    
    #
    #Functions for when moving:
    #

    #arrive at a station
    def arriveAt(self, station, time, totalTime):
        self._atStation = station
        self._cameFrom = self._movingFrom
        self._movingTo = 0
        self._movingFrom = 0
        self._distanceToStation = 0
        self._distanceMovedTowardsStation = 0
        self._distanceFromStationToDecelerate = 0
        self._moving = False

        # if self._line == 'f-line' and self._uid == '7':
        #     print(f"Train: {self._uid} arrived at station: {self._atStation.name} after running for {(totalTime-time)/60} minutes")

        self.disembarkPassengers(station,totalTime)
        station.add_carrier(self)
        if self.empty:
            self.empty = False
            station.incomingCarriers -= 1

        return time

    def passThroughStation(self, connections):
        #print(f"Carrier {self._uid} is passing through station {self._movingTo}")

        self._movingFrom = self._movingTo
        self._movingTo = self._path.pop(0)
        self._distanceMovedTowardsStation = 0

        if (self._movingFrom,self._movingTo) in connections:
            self._distanceToStation = connections[(self._movingFrom,self._movingTo)].distance
        elif (self._movingTo,self._movingFrom) in connections:
            self._distanceToStation = connections[(self._movingTo,self._movingFrom)].distance
        else:
            print(f"Carrier {self._uid} is fucked, connection does not exist")

        self.calculateAccelerateTo(self._distanceToStation)


    #Keep moving alon the track towards the next station
    def keepMoving(self, time, totalTime, connections):
        if self._shouldStop:
            self.decelerate(time)
            return 0

        if (self._speed < self._maxSpeed and not self._decelerating):
            time = self.accelerate(time)

        if (self._decelerating):
            time = self.decelerate(time)
            if self._speed == 0:
                time = self.arriveAt(self._destination, time, totalTime)
            return time

        #If we're moving towards our destination, we should brake
        if self._movingTo == self._destination.name:

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
                time = self.arriveAt(self._destination,time, totalTime)

        #Else we should just move through the station at max speed
        else:
            if (self._distanceMovedTowardsStation + time * self._speed < self._distanceToStation):
                self._distanceMovedTowardsStation += time * self._speed
                return 0
            
            for i in range(time):
                if (self._distanceMovedTowardsStation + i * self._speed >= self._distanceToStation):
                    self._distanceMovedTowardsStation += i * self._speed
                    time -= i
                    break
            
            self.passThroughStation(connections)
            time = self.keepMoving(time,totalTime,connections)

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

    
    #Other getters and functions
    def moving(self):
        return self._moving

    def availablePassengerSpace(self):
        return self._maxPassengers - len(self._passengers)

    def printInformation(self):
        print(f"uid: {self._uid}")
        print(f"speed: {self._speed}")
        print(f"atStation: {self._atStation}")
        print(f"cameFrom: {self._cameFrom}")
        print(f"moving: {self._moving}")
        print(f"movingTo: {self._movingTo}")
        print(f"movingFrom: {self._movingFrom}")
        print(f"distanceToStation: {self._distanceToStation}")
        print(f"distanceMovedTowardsStation: {self._distanceMovedTowardsStation}")
        print(f"distanceFromStationToDecelerate: {self._distanceFromStationToDecelerate}")
        print(f"passengers: {len(self._passengers)}")
        print(f"availablePassengerSpace: {self.availablePassengerSpace()}")

    def getUID(self):
        return self._uid