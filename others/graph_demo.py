import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import json
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
# connections_file = os.path.join(dirname, '../assets/connections.json')
stations_file = os.path.join(dirname, '../assets/stations.json')

from train_simulation.Railway import Connection
from train_simulation.Railway import Station

def get_trace_points(point1, point2, step):
    l = np.arange (0, 1+step, step)
    return (l*point2[0]+(1-l)*point1[0]), (l*point2[1]+(1-l)*point1[1])

def update_point(n, x, y, point):
    point.set_data(np.array([x[n], y[n]]))
    return point

# connections_file = open(connections_file, mode="r", encoding="utf-8")
stations_file = open(stations_file, mode="r", encoding="utf-8")

# connections = json.load(connections_file, object_hook=Connection.from_json)

stations_json = json.load(stations_file)
stations = []
for s in stations_json:
    stations.append(Station(s,stations_json[s]['X'],stations_json[s]['Y'],0))

fig, ax = plt.subplots()

G = nx.Graph()
for s in stations:
    G.add_node(s.name, pos=(s.x, s.y))

pos=nx.get_node_attributes(G,'pos')
# for s in connections:
#     G.add_edge(s.station_start.name, s.station_end.name, length = s.distance)
# pos = nx.planar_layout(G,scale=100)
# # pos["Lyngby"] = (0,0)
# # pos["Jærgenborg"] = (10,4)

# x, y = get_trace_points(pos["Hillerød"], pos["Allerød"], 0.01)
# x0, y0 = get_trace_points(pos["Allerød"], pos["Birkerød"], 0.01)
# x1, y1 = get_trace_points(pos["Birkerød"], pos["Holte"], 0.01)
# x2, y2 = get_trace_points(pos["Holte"], pos["Virum"], 0.01)
# x3, y3 = get_trace_points(pos["Virum"], pos["Sorgenfri"], 0.01)
# x4, y4 = get_trace_points(pos["Sorgenfri"], pos["Lyngby"], 0.01)
# x5, y5 = get_trace_points(pos["Lyngby"], pos["Jærgenborg"], 0.01)
# x6, y6 = get_trace_points(pos["Jærgenborg"], pos["Gentofte"], 0.01)
# x7, y7 = get_trace_points(pos["Gentofte"], pos["Bernstoftevej"], 0.01)

# x = np.concatenate((x,x0,x1,x2,x3,x4,x5,x6,x7))
# y = np.concatenate((y,y0,y1,y2,y3,y4,y5,y6,y7))

# train, = ax.plot([x[0]], [y[0]], 'x', color='r')

# ani=FuncAnimation(fig, update_point, 900, fargs=(x, y, train), interval=10)

nx.draw(G, pos, node_size=3, node_color='w')
img = mpimg.imread(os.path.join(dirname, '../assets/map_dots.png'))
imgplot = plt.imshow(img)

plt.show()
