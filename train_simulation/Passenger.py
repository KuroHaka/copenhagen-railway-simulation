from datetime import datetime
import uuid

class Passenger:
    _destination = 'destination not set'
    _currentlocation = 'currentlocation not set'
    _departureTime = datetime
    _id = ''
    #is travel time needed?
    _travelTimeEnd = datetime
    _travelTime = datetime
    _isArrived = bool

    def __init__(self,currentlocation,destination,departuetime):
        self._currentlocation = currentlocation
        self._destination = destination
        self._departureTime = departuetime
        self._id = uuid.uuid4()
        self._isArrived = False

    def getdestination(self):
        return self._destination

    def getlocation(self):
        return self._currentlocation
    
    def getdepartureTime(self):
        return self._departureTime
    
    def getid(self):
        return self._id


    def setdestination(self, newdestination):
         self._destination = newdestination
    
    def setlocation(self, newlocation):
         self._destination = newlocation
    
    def setdepartureTime(self, newdepartueTime):
         self._destination = newdepartueTime
        
    def printInformation(self):
        print(f"id: {self._id}")
        print(f"current location: {self._currentlocation}")
        print(f"destination: {self._destination}")
        print(f"departuretime: {self._departureTime}")
        if self._isArrived:
            print(f"travel time: {self._travelTime}")

    def isArrived(self):
        if(self._departureTime==self._departureTime):  
            self._travelTimeEnd = datetime.now()
            self._travelTime = self._travelTimeEnd - self._departureTime  
            self._isArrived = True



#Testing delete this
import time

p1 = Passenger('Lyngby','kbh h',datetime.now())
print('test')
p1.printInformation()

p1.setlocation('kbh h')
time.sleep(3)
p1.isArrived()
p1.printInformation()


