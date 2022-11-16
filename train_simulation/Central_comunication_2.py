import simpy
import os, sys, json
from train_simulation.Moving import Carrier
from train_simulation.Railway import Station, Connection, Stations, Connections

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
connectionFilePath = os.path.join(dirname, '../assets/stations.json')
trainsFilePath = os.path.join(dirname, '../assets/trains.json')

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


def carriers(env):
    return 


def main():
    env=simpy.Environment()    #creat an instance of environment
    env.process(carriers(env))   #the instance is passed into our carriers process function
    carriers=Carriers(env)  #creat one carriers
    env.run(until=30)  #start the simulation by "run()", and passing an end time 30 to it
    return

if __name__ == "__main__":
    main()


