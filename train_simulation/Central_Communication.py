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
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import networkx as nx
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
connectionFilePath = os.path.join(dirname, '../assets/connections.json')
trainsFilePath = os.path.join(dirname, '../assets/trains.json')

from train_simulation.Moving import Train
from train_simulation.Railway import *
from train_simulation.Person import Person

connections = []
trains = {}

def initSim():

    global connections
    global trains

    with open(connectionFilePath, mode="r", encoding="utf-8") as connectionsFile:
        connections = json.load(connectionsFile, object_hook=Connection.from_json)

    with open(trainsFilePath, mode="r", encoding="utf-8") as trainsFile:
        trainsArray = json.load(trainsFile, object_hook=Train.loadFromJSON)
        for train in trainsArray:
            trains[train.getUID()] = train


#tickLength is the amount of "seconds" every tick
def tickTrain(tickLength):
    for train in trains:
        timeLeft = tickLength

        #If the train is moving, it needs to comtinue doing so (this can make the train arrive at a station, without using all whole tickLength)
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
                for connection in connections:
                    if atStation == connection.station_start.name or atStation == connection.station_end.name:
                        if nextStation == connection.station_start.name or nextStation == connection.station_end.name:
                            distance = connection.distance
                            break
            
            #Find the next connection and move to next station
            else:
                for connection in connections:
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

            trains[train].moveTo(nextStation,distance,timeLeft)
            #print(nextStation,distance)


#def tickCarrier(speed):

def printAllTrainInformation():
    for train in trains:
        trains[train].printInformation()
        print()

fig, ax = plt.subplots()

def get_map_position(station_a:Station, station_b:Station, moved_distance:float, total_dictance:float) -> (float, float):
    l = moved_distance/total_dictance
    return (l*station_b.x+(1-l)*station_a.x), (l*station_b.y+(1-l)*station_a.y)

def update_train_positions(n, points, plotter):
    for i in range(len(plotter)):
        plotter[i].set_data(np.array([points[i][0][n],points[i][1][n]]))

def animate(n, points):
    ax.clear()
    for p in points:
        ax.plot([p[0][n]], [p[1][n]], '.', color='r')


def main():
    #pygame.init()
    initSim()
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'

    if (animation):
        stations_file = os.path.join(dirname, '../assets/stations.json')
        stations_file = open(stations_file, mode="r", encoding="utf-8")
        stations_json = json.load(stations_file)
        stations = {}
        #getting all stations from json
        for s in stations_json:
            stations[s] = Station(s,stations_json[s]['X'],stations_json[s]['Y'],0)
        G = nx.Graph()
        #insert all stations in the graph
        for s in stations:
            G.add_node(stations[s].name, pos=(stations[s].x, stations[s].y))
        pos=nx.get_node_attributes(G,'pos')

        #calculate the animation as an array
        x0 = []
        y0 = []
        x1 = []
        y1 = []
        for i in range(200):
            if trains['0']._moving:
                new_x, new_y = get_map_position(
                        stations[trains['0']._movingFrom], 
                        stations[trains['0']._movingTo], 
                        trains['0']._distanceMovedTowardsStation, 
                        trains['0']._distanceToStation)
                x0.append(new_x)
                y0.append(new_y)
            else:
                x0.append(stations[trains['0']._atStation].x)
                y0.append(stations[trains['0']._atStation].y)
            if trains['1']._moving:
                new_x, new_y = get_map_position(
                        stations[trains['1']._movingFrom], 
                        stations[trains['1']._movingTo], 
                        trains['1']._distanceMovedTowardsStation, 
                        trains['1']._distanceToStation)
                x1.append(new_x)
                y1.append(new_y)
            else:
                x1.append(stations[trains['1']._atStation].x)
                y1.append(stations[trains['1']._atStation].y)
            tickTrain(10)
            
        #setup color, shape, and initial position
        nx.draw(G, pos, node_size=3, node_shape='.',  node_color='black')
        t1, = ax.plot([x0[0]], [y0[0]], 'x', color='r')
        t2, = ax.plot([x1[0]], [y1[0]], 'x', color='r')
        trains_dots = [[(x0,y0),(x1,y1)],[t1,t2]]
        ani=FuncAnimation(fig, update_train_positions, len(x0), fargs=(trains_dots), interval=1, repeat=False)
        #plot all the dots for stations
        #plot background image
        img = mpimg.imread(os.path.join(dirname, '../assets/map_minmal.png'))
        imgplot = plt.imshow(img)
        # ani.save("simple_animation.gif", dpi=300, writer=PillowWriter(fps=1))
        plt.show()
    else:
        for i in range(20):
            trains['0'].printInformation()
            tickTrain(60)
            print()
    return


if __name__ == "__main__":
    main()