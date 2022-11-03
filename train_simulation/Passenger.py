from datetime import datetime
import uuid

class Passenger:
    _destination = 'destination not set'
    _currentlocation = 'currentlocation not set'
    _departureTime = datetime
    _id = ''
    #is travel time needed?
    _travelTime = datetime

    def __init__(self,currentlocation,destination,departuetime):
        self._currentlocation = currentlocation
        self._destination = destination
        self._departureTime = departuetime
        self._id = uuid.uuid4()

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


#Testing delete this
import PassengerGroup


p1 = Passenger('Lyngby','kbh h',datetime.now())
print('test')
p1.printInformation()
p2 = Passenger('Lyngby','1',datetime.now())
p3 = Passenger('Lyngby','2',datetime.now())
p4 = Passenger('Lyngby','3',datetime.now())

grouparray = Passenger[p1,p2,p3,p4]
g1 = PassengerGroup(grouparray)

print(g1)


#

