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
        Turn the train at the end of the line
"""

import os, sys, json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from train_simulation.Moving import Train
from train_simulation.Railway import Station, Connection, Stations, Connections, Lines
from Person import Passenger

class Point:
    def __init__(self,pointer):
        self.pointer = pointer
        self.x = []
        self.y = []
    def update_position(self,n):
        self.pointer.set_data(np.array([self.x[n],self.y[n]]))

class Simulation:

    trains = {}
    pointers = {}
    fig, ax = plt.subplots()

    def __init__(self):
        stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8")
        json.load(stations_file, object_hook=Station.from_json)

        new_connections_file = open(os.path.join(dirname, '../assets/new_connections.json'), mode="r", encoding="utf-8")
        json.load(new_connections_file, object_hook=Connection.from_json)

        with open(os.path.join(dirname, '../assets/lines.json'), mode="r", encoding="utf-8") as linesFile:
            self.lines = json.load(linesFile)

        self.stations = Stations
        self.connections = Connections
        self.G = nx.Graph()
        self.cumulativeTick = 0
        self.allPassengersGenerated = []
        self.generateTrains(52)

    def tickPersonGeneration(self, weight, tickLength):
        self.cumulativeTick += tickLength
        for _, station in self.stations.items():
            passenger = Passenger(station,'København H',self.cumulativeTick)
            station.add_passenger(passenger)
            self.allPassengersGenerated.append(passenger)

    def generateTrains(self, numberOfTrains):
        trainID = 0

        aDistance = 74310
        bDistance = 48980
        cDistance = 55210
        fDistance = 11810

        #A: 9/26
        #B: 7/26  
        #C: 8/26 
        #F: 2/26

        aTrains = round(numberOfTrains * (9/26))
        bTrains = round(numberOfTrains * (7/26))
        cTrains = round(numberOfTrains * (8/26))
        fTrains = round(numberOfTrains * (2/26))

        if aTrains + bTrains + cTrains + fTrains < numberOfTrains:
            #Find largest ronuding
            roundA = numberOfTrains * (9/26) - aTrains
            roundB = numberOfTrains * (7/26) - bTrains
            roundC = numberOfTrains * (8/26) - cTrains
            roundF = numberOfTrains * (2/26) - fTrains

            if roundA > max(roundB,roundC,roundF):
                aTrains += 1
            elif roundB > max(roundA,roundC,roundF):
                bTrains += 1
            elif roundC > max(roundA,roundB,roundF):
                cTrains += 1
            elif roundF > max(roundA,roundC,roundB):
                fTrains += 1


        elif aTrains + bTrains + cTrains + fTrains > numberOfTrains:
            roundA = aTrains - numberOfTrains * (9/26)
            roundB = bTrains - numberOfTrains * (7/26)
            roundC = cTrains - numberOfTrains * (8/26)
            roundF = fTrains - numberOfTrains * (2/26)

            if roundA > max(roundB,roundC,roundF):
                aTrains -= 1
            elif roundB > max(roundA,roundC,roundF):
                bTrains -= 1
            elif roundC > max(roundA,roundB,roundF):
                cTrains -= 1
            elif roundF > max(roundA,roundC,roundB):
                fTrains -= 1

        mapOTrains = {'a': aTrains, 'b': bTrains, 'c': cTrains, 'f': fTrains}
        rangeBetweenTrains = {}

        rangeBetweenTrains['a'] = aDistance // (aTrains/2 + 1)
        rangeBetweenTrains['b'] = bDistance // (bTrains/2 + 1)
        rangeBetweenTrains['c'] = cDistance // (cTrains/2 + 1)
        rangeBetweenTrains['f'] = fDistance // (fTrains/2 + 1)

        print(rangeBetweenTrains)


        for line in self.lines.keys():
            self.trains[str(trainID)] = Train(str(trainID), self.stations[self.lines[line][0]], self.stations[self.lines[line][1]], line)
            trainID += 1
            
            mapOTrains[line] -= 1
            if mapOTrains[line] == 0:
                continue

            self.trains[str(trainID)] = Train(str(trainID), self.stations[self.lines[line][-1]], self.stations[self.lines[line][-2]], line)
            trainID += 1

            mapOTrains[line] -= 1
            if mapOTrains[line] == 0:
                continue


            distanceMoved = 0
            for i in range(len(self.lines[line])-1):
                if (self.lines[line][i],self.lines[line][i+1]) in self.connections:
                    if distanceMoved > rangeBetweenTrains[line]:
                        self.trains[str(trainID)] = Train(str(trainID), self.stations[self.lines[line][i]], self.stations[self.lines[line][i+1]], line)
                        trainID += 1
                        
                        mapOTrains[line] -= 1
                        if mapOTrains[line] == 0:
                            break


                        self.trains[str(trainID)] = Train(str(trainID), self.stations[self.lines[line][i]], self.stations[self.lines[line][i-1]], line)
                        trainID += 1

                        mapOTrains[line] -= 1
                        if mapOTrains[line] == 0:
                            break

                        distanceMoved = 0
                    distanceMoved += self.connections[(self.lines[line][i],self.lines[line][i+1])].distance


                elif (self.lines[line][i+1],self.lines[line][i]) in self.connections:
                    if distanceMoved > rangeBetweenTrains[line]:
                        self.trains[str(trainID)] = Train(str(trainID), self.stations[self.lines[line][i]], self.stations[self.lines[line][i+1]], line)
                        trainID += 1

                        mapOTrains[line] -= 1
                        if mapOTrains[line] == 0:
                            break

                        self.trains[str(trainID)] = Train(str(trainID), self.stations[self.lines[line][i]], self.stations[self.lines[line][i-1]], line)
                        trainID += 1

                        mapOTrains[line] -= 1
                        if mapOTrains[line] == 0:
                            break

                        distanceMoved = 0
                    distanceMoved += self.connections[(self.lines[line][i+1],self.lines[line][i])].distance

    def generateTrainsFromJson():
        with open(os.path.join(dirname, '../assets/trains.json'), mode="r", encoding="utf-8") as trainsFile:
            trainsArray = json.load(trainsFile, object_hook=Train.loadFromJSON)
            for train in trainsArray:
                self.trains[train.getUID()] = train
                self.trains[train.getUID()]._atStation = self.stations[train._atStation]
                self.trains[train.getUID()]._movingTo = self.stations[train._movingTo]

    #tickLength is the amount of "seconds" every tick
    def tickTrain(self, tickLength):
        skip = False
        for key, train in self.trains.items():
            timeLeft = tickLength

            #If the train is moving, it needs to comtinue doing so (this can make the train arrive at a station, without using the whole tickLength)
            if train.moving():
                timeLeft = train.keepMoving(timeLeft,self.cumulativeTick)

            #If train is at a station, we need to find where to go next
            if not train.moving():
                nextStation = None
                distance = None
                cameFrom, atStation = train.cameFromAtStation()

                #This case is needed when trains are just initialised
                if not cameFrom:
                    _, nextStation = train.goingFromTo()

                    for _,connection in self.connections.items():

                        if atStation == connection.station_start or atStation == connection.station_end:
                            if nextStation == connection.station_start or nextStation == connection.station_end:
                                distance = connection.distance
                                break
                
                #Find the next connection and move to next station
                else:
                    for _,connection in self.connections.items():
                        if atStation == connection.station_start or atStation == connection.station_end:
                            if cameFrom == connection.station_start or cameFrom == connection.station_end:
                                continue
                            if atStation != connection.station_start:
                                if connection.station_start.name not in self.lines[train._line]:
                                    #print(f"Station {connection.station_start.name} not part of line {trains[train]._line}")
                                    continue
                                nextStation = self.stations[connection.station_start.name]
                                distance = connection.distance
                                break
                            elif atStation != connection.station_end:
                                if connection.station_end.name not in self.lines[train._line]:
                                    #print(f"Station {connection.station_end.name} not part of line {trains[train]._line}")
                                    continue
                                nextStation = self.stations[connection.station_end.name]
                                distance = connection.distance
                                break
            
                #If we cannot find a connection, we must be at the end of the line, and we have to turn around
                if not nextStation:
                    (nextStation,distance) = train.turnAround()

                if not distance:
                    print(f"Distance of train {key} is fucked")

                for _,train2 in self.trains.items():
                    if train2.moving() and train != train2 and train2._movingTo == nextStation and train2._movingFrom == train._atStation:
                        skip = True
                        break
                
                train.moveTo(nextStation,distance,timeLeft, skip)
                if skip:
                    skip = False

    def get_map_position(self, station_a:Station, station_b:Station, moved_distance:float, total_dictance:float) -> (float, float):
        l = moved_distance/total_dictance
        return l*station_b.x+(1-l)*station_a.x, l*station_b.y+(1-l)*station_a.y

    def update_train_positions(self, n):
        for _, plotter in self.pointers.items():
            plotter.update_position(n)

    def run_simulation(self, epoch: int, tick_lenght: int):
        for i in range(epoch):
            for _, train in self.trains.items():
                train.printInformation()
                print()
            print('------------------------------------------')
            self.tickTrain(tick_lenght)

    def printAllTrainInformation(self):
        for _,train in self.trains.items():
            train.printInformation()
            print()

    def printAllPassengersInStations(self):
        for _,station in self.stations.items():
            print(station.name, station.get_passengers())

    def run_simulation_with_animation(self, epoch: int, tick_lenght: int, output_fig=False):
        #init stations
        for _, station in self.stations.items():
            self.G.add_node(station.name, pos=(station.x, station.y))
        pos=nx.get_node_attributes(self.G,'pos')

        for _, connection in self.connections.items():
            self.G.add_edge(connection.station_start.name, connection.station_end.name)

        #init pointers
        for key, train in self.trains.items():
                if train._moving:
                    newx, newy = self.get_map_position(
                            self.stations[train._movingFrom.name], 
                            self.stations[train._movingTo.name], 
                            train._distanceMovedTowardsStation, 
                            train._distanceToStation)
                    p, = self.ax.plot(newx, newy, 'x', color='r')
                    self.pointers[key] = Point(p)
                else:
                    starting = self.stations[train._atStation.name]
                    p, = self.ax.plot(starting.x, starting.y, 'x', color='r')
                    self.pointers[key] = Point(p)

        for i in range(epoch):
            for key, train in self.trains.items():
                if train._moving:
                    newx, newy = self.get_map_position(
                            self.stations[train._movingFrom.name], 
                            self.stations[train._movingTo.name], 
                            train._distanceMovedTowardsStation, 
                            train._distanceToStation)
                    self.pointers[key].x.append(newx)
                    self.pointers[key].y.append(newy)
                else:
                    self.pointers[key].x.append(self.stations[train._atStation.name].x)
                    self.pointers[key].y.append(self.stations[train._atStation.name].y)
            self.tickTrain(tick_lenght)

        ani=FuncAnimation(self.fig, self.update_train_positions, epoch, interval=1, repeat=False)
        
        nx.draw(self.G, pos, node_size=4, node_shape='.',  edge_color='gray' ,node_color='black')
        img = mpimg.imread(os.path.join(dirname, '../assets/map_minmal.png'))
        imgplot = plt.imshow(img)
        if output_fig:
            ani.save(os.path.join(dirname, '../assets/animation.gif'), writer='imagemagick', fps=30)
        else:
            self.fig.tight_layout()
            plt.show()
                
                