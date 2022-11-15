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
from train_simulation.Railway import Station, Connection, Stations, Connections

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

        self.stations = Stations
        self.connections = Connections
        self.G = nx.Graph()

        with open(os.path.join(dirname, '../assets/trains.json'), mode="r", encoding="utf-8") as trainsFile:
            trainsJson = json.load(trainsFile, object_hook=Train.loadFromJSON)
            for train in trainsJson:
                self.trains[train.getUID()] = train

    def tickTrain(self, tickLength):
        for train in self.trains:
            timeLeft = tickLength

            #If the train is moving, it needs to comtinue doing so (this can make the train arrive at a station, without using all whole tickLength)
            if self.trains[train].moving():
                timeLeft = self.trains[train].keepMoving(timeLeft)

            #If train is at a station, we need to find where to go next
            if not self.trains[train].moving():
                nextStation = None
                distance = None
                cameFrom, atStation = self.trains[train].cameFromAtStation()

                #This case is needed when trains are just initialised
                if not cameFrom:
                    _, nextStation = self.trains[train].goingFromTo()
                    for _,connection in Connections.items():
                        if atStation == connection.station_start.name or atStation == connection.station_end.name:
                            if nextStation == connection.station_start.name or nextStation == connection.station_end.name:
                                distance = connection.distance
                                break
                
                #Find the next connection and move to next station
                else:
                    for _,connection in Connections.items():
                        if atStation == connection.station_start.name or atStation == connection.station_end.name:
                            if cameFrom == connection.station_start.name or cameFrom == connection.station_end.name:
                                continue
                            if atStation != connection.station_start.name:
                                nextStation = connection.station_start.name
                                distance = connection.distance
                                break
                            elif atStation != connection.station_end.name:
                                nextStation = connection.station_end.name
                                distance = connection.distance
                                break

                if not nextStation or not distance:
                    print(f"Something wrong with train {train}")

                self.trains[train].moveTo(nextStation,distance,timeLeft)

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

    def run_simulation_with_animation(self, epoch: int, tick_lenght: int, output_fig=False):
        #init stations
        for _, station in self.stations.items():
            self.G.add_node(station.name, pos=(station.x, station.y))
        pos=nx.get_node_attributes(self.G,'pos')

        for _, connection in self.connections.items():
            self.G.add_edge(connection.station_start.name, connection.station_end.name)

        #init pointers
        for key, train in self.trains.items():
            starting = self.stations[train._atStation]
            p, = self.ax.plot(starting.x, starting.y, arrowprops=dict(arrowstyle="->"), color='r')
            self.pointers[key] = Point(p)

        for i in range(epoch):
            for key, train in self.trains.items():
                if train._moving:
                    newx, newy = self.get_map_position(
                            self.stations[train._movingFrom], 
                            self.stations[train._movingTo], 
                            train._distanceMovedTowardsStation, 
                            train._distanceToStation)
                    self.pointers[key].x.append(newx)
                    self.pointers[key].y.append(newy)
                else:
                    self.pointers[key].x.append(self.stations[train._atStation].x)
                    self.pointers[key].y.append(self.stations[train._atStation].y)
            self.tickTrain(tick_lenght)

        ani=FuncAnimation(self.fig, self.update_train_positions, epoch, interval=1, repeat=False)
        
        nx.draw(self.G, pos, node_size=4, node_shape='.',  edge_color='gray' ,node_color='black')
        img = mpimg.imread(os.path.join(dirname, '../assets/map_minmal.png'))
        imgplot = plt.imshow(img)
        if output_fig:
            ani.save(os.path.join(dirname, '../assets/animation.gif'), writer='imagemagick', fps=30)
        else:
            plt.show()
                
                
