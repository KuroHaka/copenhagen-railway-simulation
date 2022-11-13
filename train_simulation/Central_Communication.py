""" Thoughts:
        Connections need a LINE(S)
        Trains need a LINE

        Connections can be made into a dictionary with LINE as key and array of connection on this LINE as value
        This will make sure that a train, running on a specific line, does not suddenly change line because connections are ambiguous
        And make the algorithm faster

        Backend will run in TICKS where each TICK is x amount of seconds
        If a TICK is 60 second then every train will "spend" 60 second doing whatever (accelerating, waiting, simply moving)
        These seconds will carry over to next task if every second in a tick is not spent 
        For example: If we only need to wait at a station for 30 seonds more, we can then spend the last 30 seonds of the TICK accelerating

        TICK = 60s
        The train class will have a single function that "runs" the train:
            The first part of the function could be waiting at a station if we need to wait for 150s then we call this function so many times where every time it "costs" a second
            At the third TICK the train is done waiting, but it still has 30s left, these 30s can then be used to accelerate, 
            where every call to accelerate "costs" a second (and accelerates the train with 1.3m/s)

            Then maybe at the 6th TICK we are done accelerating and still have 15s left of the TICK, then we simply move the train along its path this many times (we calculate the trains speed in m/s)

            And so forth

            The functions does not need to be called once for every second, they can calculate how much time is needed and then just subtract that from the amount of seconds there is left

        If this function is in the train class, it will probably not work, since the train does not know of passengers at the train stations.
        We can't TICK the trains and the stations seperately, it has to be done together (unless the train know of all passengers of all stations)

        Can the same idea be done in this file?
        
    

    #TODO
        Turn around train -- DONE
        Board/disembark passengers -- DONE (though they are just numbers right now)
        
        Collision detection -- Made a rudementray collision avoidance, a train wont move onto a connection, if there is another train there (accounts for direction).

        Generate passengers -- we generate some numbers
"""


import os, sys, json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
stationsFilePath = os.path.join(dirname, '../assets/stations.json')
connectionsFilePath = os.path.join(dirname, '../assets/connections.json')
trainsFilePath = os.path.join(dirname, '../assets/trains.json')

from train_simulation.Moving import Train
from train_simulation.Railway import Station, Connection, Stations, Connections
from train_simulation.Person import Passenger

trains = {}
allPassengersGenerated = []

cumulativeTick = 0

def initSim():
    
    stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8")
    json.load(stations_file, object_hook=Station.from_json)

    new_connections_file = open(os.path.join(dirname, '../assets/new_connections.json'), mode="r", encoding="utf-8")
    json.load(new_connections_file, object_hook=Connection.from_json)

    with open(trainsFilePath, mode="r", encoding="utf-8") as trainsFile:
        trainsArray = json.load(trainsFile, object_hook=Train.loadFromJSON)
        for train in trainsArray:
            trains[train.getUID()] = train
            trains[train.getUID()]._atStation = Stations[train._atStation]
            trains[train.getUID()]._movingTo = Stations[train._movingTo]


#Tick the generation of people
def tickPersonGeneration(weight, tickLength):
    global cumulativeTick
    cumulativeTick += tickLength
    # for station in stations:
    #     stations[station].add_passengers(round(10*weight*(tickLength/60)))
    passenger = Passenger('Hillerød','Bernstorffsvej',cumulativeTick)
    Stations['Hillerød'].add_passenger(passenger)
    allPassengersGenerated.append(passenger)



#tickLength is the amount of "seconds" every tick
def tickTrain(tickLength):
    skip = False
    for train in trains:
        timeLeft = tickLength

        #If the train is moving, it needs to comtinue doing so (this can make the train arrive at a station, without using the whole tickLength)
        if trains[train].moving():
            timeLeft = trains[train].keepMoving(timeLeft)

        #If train is at a station, we need to find where to go next
        if not trains[train].moving():
            nextStation = None
            distance = None
            cameFrom, atStation = trains[train].cameFromAtStation()

            #This case is needed when trains are just initialised
            if not cameFrom:
                _, nextStation = trains[train].goingFromTo()

                for _,connection in Connections.items():

                    if atStation == connection.station_start or atStation == connection.station_end:
                        if nextStation == connection.station_start or nextStation == connection.station_end:
                            distance = connection.distance
                            break
            
            #Find the next connection and move to next station
            else:
                for _,connection in Connections.items():
                    if atStation == connection.station_start or atStation == connection.station_end:
                        if cameFrom == connection.station_start or cameFrom == connection.station_end:
                            continue
                        if atStation != connection.station_start:
                            nextStation = Stations[connection.station_start.name]
                            distance = connection.distance
                            break
                        elif atStation != connection.station_end:
                            nextStation = Stations[connection.station_end.name]
                            distance = connection.distance
                            break
            
            #If we cannot find a connection, we must be at the end of the line, and we have to turn around
            if not nextStation:
                print(f"Train: {train} turned around")
                (nextStation,distance) = trains[train].turnAround()

            if not distance:
                print(f"Distance of train {train} is fucked")

            for train2 in trains:
                if trains[train2].moving() and train != train2 and trains[train2]._movingTo == nextStation and trains[train2]._movingFrom == trains[train]._atStation:
                    skip = True
                    break
            
            trains[train].moveTo(nextStation,distance,timeLeft, skip)
            if skip:
                skip = False

#def tickCarrier(speed):

def printAllTrainInformation():
    for train in trains:
        trains[train].printInformation()
        print()

def printAllPassengersInStations():
    for station in stations:
        print(stations[station].name, stations[station].passengers)

def main():
    #pygame.init()

    weight = 1
    tickLength = 60


    initSim()

    #print(Stations)

    #for (names,end),_ in Connections.items():
    #    print(names)

    # tickPersonGeneration(1,60)
    # print(stations['Hillerød'].passengers)
    # tickTrain(tickLength)
    # print(stations['Hillerød'].passengers)
    # printAllTrainInformation()

    #print(trains)

    for i in range(60):
        #trains['0'].printInformation()
        printAllTrainInformation()
        #printAllPassengersInStations()
        print()
        tickPersonGeneration(weight,tickLength)
        tickTrain(tickLength)
        print()


    return


if __name__ == "__main__":
    main()