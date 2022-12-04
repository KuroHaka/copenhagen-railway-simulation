from Algorithms import Algorithms
from datetime import timedelta
import os, sys, json, simpy, enum, uuid
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from carriers_simulation.Rail_Transport import Carrier
from carriers_simulation.Railway import Connection, Station, Connections, Stations
from carriers_simulation.Person import Person, Passengers, getFirstPersonTime

class Simulation:

    Carriers = []
    G = nx.Graph()

    def __init__(self):
        self.env = simpy.Environment()
        stations_file = open(
            os.path.join(dirname, "../assets/new_stations.json"), mode="r", encoding="utf-8"
        )
        json.load(stations_file, object_hook=Station.from_json)
        new_connections_file = open(
            os.path.join(dirname, "../assets/new_connections.json"), mode="r", encoding="utf-8"
        )
        json.load(new_connections_file, object_hook=Connection.from_json)
        new_passengers_file = open(
            os.path.join(dirname, "../assets/passengers.json"), mode="r", encoding="utf-8"
        )
        json.load(new_passengers_file, object_hook=Person.from_json)
    
    def run_carriers_simulation(self, duration, num_carriers = len(Stations)*5, baseTickTime = 1):
        env = simpy.Environment()
        # get start 
        simulation_start = getFirstPersonTime()

        for p in Passengers:
            env.process(Stations[p.start_station].loadPassenger(p))

        for _, station in Stations.items():
            station.setEnvironment(env,baseTickTime,simulation_start)
            for i in range(5):
                c = Carrier(uuid.uuid4(), station, baseTickTime, Stations, Connections, env)
                env.process(c.deploy())
                self.Carriers.append(c)
        
        for c in self.Carriers:
            env.process(c.printEvents())
        env.run(until=duration)

    def update_animation(self, figure, env, tick_lenght):
        while True:
            figure.canvas.draw()
            figure.canvas.flush_events()
            yield env.timeout(tick_lenght)

    def run_carriers_simulation_animation(self, duration, tick_lenght, num_carriers = len(Stations)*5, baseTickTime = 1):
        env = simpy.Environment()
        plt.ion()
        for _, station in Stations.items():
            self.G.add_node(station.name, pos=(station.x, station.y))
        pos=nx.get_node_attributes(self.G,'pos')
        for _, Pairs in Connections.items():
            for _, connection in Pairs.items():
                self.G.add_edge(connection.station_start.name, connection.station_end.name)
        figure, ax = plt.subplots(figsize=(10, 18))
        img = mpimg.imread(os.path.join(dirname, '../assets/map_minmal.png'))
        imgplot = plt.imshow(img)
        nx.draw(self.G, pos, node_size=4, node_shape='.',  edge_color='gray' ,node_color='black')
        
        simulation_start = getFirstPersonTime()

        for p in Passengers:
            env.process(Stations[p.start_station].loadPassenger(p))

        for _, station in Stations.items():
            station.setEnvironment(env,baseTickTime,simulation_start)
            for i in range(1):
                c = Carrier(uuid.uuid4(), station, baseTickTime, Stations, Connections, env)
                env.process(c.deploy())
                self.Carriers.append(c)
        print("environment set")
        print(self.Carriers)

        env.process(c.updatePlotPosition(tick_lenght))
        env.process(self.update_animation(figure, env, tick_lenght))

        env.run(until=duration)