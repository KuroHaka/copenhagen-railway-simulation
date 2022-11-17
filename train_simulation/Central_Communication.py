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
from Algorithms import Algorithms
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
connectionFilePath = os.path.join(dirname, '../assets/stations.json')
trainsFilePath = os.path.join(dirname, '../assets/trains.json')

from train_simulation.Moving import Train
from train_simulation.Railway import Station, Connection, Stations, Connections, Lines

connections = []
trains = {}

def initSim():
    
    stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8")
    json.load(stations_file, object_hook=Station.from_json)

    new_connections_file = open(os.path.join(dirname, '../assets/new_connections.json'), mode="r", encoding="utf-8")
    json.load(new_connections_file, object_hook=Connection.from_json)

    with open(trainsFilePath, mode="r", encoding="utf-8") as trainsFile:
        trainsArray = json.load(trainsFile, object_hook=Train.loadFromJSON)
        for train in trainsArray:
            trains[train.getUID()] = train

def main():
    #pygame.init()

    initSim()
    algo = Algorithms(Connections, Stations, Lines)
    path = algo.get_path_trains('Flintholm','Allerød')
    for p in path:
        print("--------------------")
        print('take line '+p["line"])
        print("--------------------")
        [print(x) for x in p["path"]]
    return


if __name__ == "__main__":
    main()
