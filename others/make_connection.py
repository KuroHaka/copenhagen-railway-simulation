import json, os, sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
connections_file = open(os.path.join(dirname, '../assets/connections.json'), mode="r", encoding="utf-8")
line_file = open(os.path.join(dirname, '../assets/lines.json'), mode="r", encoding="utf-8")
lines = json.load(line_file)
connections = json.load(connections_file)

def find_distance(connections, c1, c2):
    for c in connections:
        if(connections[c]['station A'] == c1 and connections[c]['station B'] == c2):
            return connections[c]['distance']
print(lines['a-line'])