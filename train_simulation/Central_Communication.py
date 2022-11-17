from Simulation import Simulation
import sys
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

from train_simulation.Moving import Train
from train_simulation.Railway import Station, Connection, Stations, Connections
from train_simulation.Person import Passenger

trains = {}
lines = {}
allPassengersGenerated = []

cumulativeTick = 0

def initSim():

    global lines
    
    with open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8") as stations_file:
        json.load(stations_file, object_hook=Station.from_json)

    with open(os.path.join(dirname, '../assets/new_connections.json'), mode="r", encoding="utf-8") as new_connections_file:
        json.load(new_connections_file, object_hook=Connection.from_json)

    with open(os.path.join(dirname, '../assets/lines.json'), mode="r", encoding="utf-8") as linesFile:
        lines = json.load(linesFile)


#Tick the generation of people
def tickPersonGeneration(weight, tickLength):
    global cumulativeTick
    cumulativeTick += tickLength
    for station in Stations:
        passenger = Passenger(station,'København H',cumulativeTick)
        Stations[str(station)].add_passenger(passenger)
        allPassengersGenerated.append(passenger)



#tickLength is the amount of "seconds" every tick
def tickTrain(tickLength):
    skip = False
    for train in trains:
        timeLeft = tickLength

        #If the train is moving, it needs to comtinue doing so (this can make the train arrive at a station, without using the whole tickLength)
        if trains[train].moving():
            timeLeft = trains[train].keepMoving(timeLeft,cumulativeTick)

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
                            if connection.station_start.name not in lines[trains[train]._line]:
                                #print(f"Station {connection.station_start.name} not part of line {trains[train]._line}")
                                continue
                            nextStation = Stations[connection.station_start.name]
                            distance = connection.distance
                            break
                        elif atStation != connection.station_end:
                            if connection.station_end.name not in lines[trains[train]._line]:
                                #print(f"Station {connection.station_end.name} not part of line {trains[train]._line}")
                                continue
                            nextStation = Stations[connection.station_end.name]
                            distance = connection.distance
                            break
            
            #If we cannot find a connection, we must be at the end of the line, and we have to turn around
            if not nextStation:
                #print(f"Train: {train} turned around")
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


def calcDistances():
    aDistance = 0
    bDistance = 0
    cDistance = 0
    fDistance = 0


    for _,connection in Connections.items():
        if connection.station_start.name in lines['a-line'] and connection.station_end.name in lines['a-line']:
            aDistance += connection.distance
        if connection.station_start.name in lines['b-line'] and connection.station_end.name in lines['b-line']:
            bDistance += connection.distance
        if connection.station_start.name in lines['c-line'] and connection.station_end.name in lines['c-line']:
            cDistance += connection.distance
        if connection.station_start.name in lines['f-line'] and connection.station_end.name in lines['f-line']:
            fDistance += connection.distance

    print(aDistance,bDistance,cDistance,fDistance)
    print(aDistance/9,bDistance/7,cDistance/8,fDistance/2)

#Default made such that trains arrive approximately every 10 minutes on every line:
#90 minutes for a, that is 9 trains in every direction (18 trains)
#70 minutes for b, that is 7 trains in every direction (14 trains)
#75 minutes for c, that is 8 trains in every direction (16 trains)
#22 minutes for f, that is 2 trains in every direction (4 trains)
#Range between trains found by dividing the range of the line with the number of trains needed (plus 1, because apparently it works like that)
def generateDefaultTrains():
    trainID = 0

    aDistance = 74310
    bDistance = 48980
    cDistance = 55210
    fDistance = 11810

    #rangeBetweenTrains = {'a-line': 8257, 'b-line': 6997, 'c-line': 6901, 'f-line': 5905}
    rangeBetweenTrains = {'a-line': 7431, 'b-line': 6122, 'c-line': 6134, 'f-line': 5905}


    for line in lines.keys():
        trains[str(trainID)] = Train(str(trainID), Stations[lines[line][0]], Stations[lines[line][1]], line)
        trainID += 1
        trains[str(trainID)] = Train(str(trainID), Stations[lines[line][-1]], Stations[lines[line][-2]], line)
        trainID += 1

        distanceMoved = 0
        for i in range(len(lines[line])-1):
            if (lines[line][i],lines[line][i+1]) in Connections:
                if distanceMoved > rangeBetweenTrains[line]:
                    trains[str(trainID)] = Train(str(trainID), Stations[lines[line][i]], Stations[lines[line][i+1]], line)
                    trainID += 1
                    trains[str(trainID)] = Train(str(trainID), Stations[lines[line][i]], Stations[lines[line][i-1]], line)
                    trainID += 1
                    distanceMoved = 0
                distanceMoved += Connections[(lines[line][i],lines[line][i+1])].distance


            elif (lines[line][i+1],lines[line][i]) in Connections:
                if distanceMoved > rangeBetweenTrains[line]:
                    trains[str(trainID)] = Train(str(trainID), Stations[lines[line][i]], Stations[lines[line][i+1]], line)
                    trainID += 1
                    trains[str(trainID)] = Train(str(trainID), Stations[lines[line][i]], Stations[lines[line][i-1]], line)
                    trainID += 1
                    distanceMoved = 0
                distanceMoved += Connections[(lines[line][i+1],lines[line][i])].distance


def generateTrains(numberOfTrains):
    aDistance = 74310
    bDistance = 48980
    cDistance = 55210
    fDistance = 11810

    ATrains = 0
    BTrains = 0
    CTrains = 0
    FTrains = 0

def generateTrainsFromJson():
    with open(os.path.join(dirname, '../assets/trains.json'), mode="r", encoding="utf-8") as trainsFile:
        trainsArray = json.load(trainsFile, object_hook=Train.loadFromJSON)
        for train in trainsArray:
            trains[train.getUID()] = train
            trains[train.getUID()]._atStation = Stations[train._atStation]
            trains[train.getUID()]._movingTo = Stations[train._movingTo]


def printAllTrainInformation():
    for train in trains:
        trains[train].printInformation()
        print()

def printAllPassengersInStations():
    for station in Stations:
        print(Stations[station].name, Stations[station].get_passengers())




def main():
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    #pygame.init()

    weight = 1
    tickLength = 60

    initSim()
    generateDefaultTrains()

    # for trainID in trains:
    #     print(trains[trainID]._uid,trains[trainID]._atStation.name,trains[trainID]._movingTo.name)

    for i in range(240):
        #printAllTrainInformation()
        #printAllPassengersInStations()
        #print()
        tickPersonGeneration(weight,tickLength)
        tickTrain(tickLength)
        # print(len(Stations['Svanemøllen'].get_passengers()))
        # for trainID in trains:
        #     if trains[trainID]._atStation:
        #         print(cumulativeTick ,trains[trainID]._uid,trains[trainID]._atStation.name)
        # print()

    totalPassengerArrived = 0
    totalTravelTime = 0
    travelTimePerLine = 0
    for person in allPassengersGenerated:
        if person.isArrived():
            totalPassengerArrived += 1
            totalTravelTime += person.getTravelTime()

    print(f"A total of {totalPassengerArrived} passengers arrived at thier destination")
    print(f"It took them a total of {totalTravelTime} minutes, that is an average of {totalTravelTime/totalPassengerArrived} per passenger")
    print(f"Simulation ran for {cumulativeTick/60} minutes")


    sim = Simulation()

    if (animation):
        sim.run_simulation_with_animation(100, 40)
    else:
        sim.run_simulation(100, 30)
    return

if __name__ == "__main__":
    main()
