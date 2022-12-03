import os, sys, json, simpy, enum
from Algorithms import Algorithms
from datetime import timedelta
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from carriers_simulation.Railway import Connection, Station, Connections, Stations
from carriers_simulation.Person import Person, Passengers, getFirstPersonTime

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

env = simpy.Environment()
simulation_start = getFirstPersonTime()
for _, station in Stations.items():
    station.setEnvironment(env,1,simulation_start)

for p in Passengers:
    env.process(Stations[p.start_station].loadPassenger(p))


class CarriersStates(enum.Enum):
    IDLE = 1
    LOADING = 2
    MOVING = 3
    STOPPING = 4
    UNUSED = 0

class Carrier:

    # Max amount of passengers on Carrier
    _maxPassengers = 5
    # Max speed of Carrier in m/s
    _maxSpeed = 33.33
    # Acceleration of carrier
    _maxAcceleration = 1.3
    _maxDeaceleration = -1.2
    # Time for Passengers to load in
    _loadingDuration = 30

    # Initialisation of the carrier
    def __init__(self, uid, atStation, tickTime, stations, connections, env):
        # carriers identifier:
        self._uid = uid
        self._tickTime = tickTime
        # Algorithms:
        self._algorithms = Algorithms(connections, stations)
        # connections to update positions:
        self._connections = connections
        self._currentConnection: Connection = None
        # carrier environment:
        self._env: simpy.Environment = env
        # Passengers on the carrier
        self._passengers = []
        # Time when last trip started
        self._departureTime = 0
        # Speed of carrier
        self._speed = 0
        # Path the train should take
        self._path = []
        self._destination = ""
        self._distanceToDestination = 0
        self._distanceLeftDestination = 0
        # current acceleration
        self._acceleration = 0
        # '' when not at a station otherwise Station
        self._stations = stations
        self._atStation = atStation
        # Is the carrier moving
        self._isMoving = False
        # Is the carrier decelerating
        self._decelerating = False
        # 0 when at a station otherwise station
        self._movingTo = ""
        self._movingFrom = ""
        # Different distances
        self._distanceToStation = 0
        self._distanceMovedStation = 0
        self._breakingDistance = 0
        self.state: CarriersStates = CarriersStates.UNUSED
        self.total_distance = 0

    def deploy(self):
        # loop of the process, never stops
        while True:
            yield self._env.process(self._atStation.enqueue(self))


    def idle(self, loading):
        self.state = CarriersStates.IDLE
        with loading.request() as request:
            yield request
            yield self._env.process(self._atStation.getPassengers(self, self._maxPassengers))
            # load passengers
            self.state = CarriersStates.LOADING
            yield self._env.timeout(self._loadingDuration)

        yield self._env.process(self.departure())
        
    
    def departure(self):
        # remove full path
        # compute path from algorithms
        shortestPath = self._algorithms.get_path(self._atStation.name, self._destination)
        self._path = shortestPath.nodes
        self._distanceToDestination = shortestPath.total_cost
        self._distanceLeftDestination = self._distanceToDestination
        self._movingFrom = self._path.pop(0)
        self._movingTo = self._path.pop(0)
        self._currentConnection = self._connections[self._movingFrom][
                self._movingTo
            ]
        self._distanceToStation = self._currentConnection.distance
        yield self._env.process(self.moving())

    def moving(self):
        self.state = CarriersStates.MOVING
        self._isMoving = True
        self._acceleration = self._maxAcceleration
        self._departureTime = self._env.now
        while self._isMoving:
            yield self._env.process(self.updateNewPosition())

    def updateConnection(self):
        self._movingFrom = self._movingTo
        self._movingTo = self._path.pop(0)
        self._currentConnection = self._connections[self._movingFrom][
                self._movingTo
            ]

    def updateAcceleration(self):
        if self._distanceLeftDestination < self._breakingDistance:
            self._acceleration = self._maxDeaceleration
        elif self._speed >= self._maxSpeed:
            self._acceleration = 0
        else:
            self._acceleration = self._maxAcceleration

    def updateSpeed(self):
        # speed = speed0 + a * t
        self._speed = max(min(self._speed + self._acceleration * self._tickTime, self._maxSpeed),0)

    def updateDistance(self):
        # distance = speed0 * t + 0.5 * acceleration t^2
        distance_moved = self._speed * self._tickTime + 0.5 * self._acceleration * self._tickTime**2
        self._distanceMovedStation += distance_moved
        self._distanceLeftDestination -= distance_moved
        self.total_distance += distance_moved

    def updateNewPosition(self):
        yield self._env.timeout(self._tickTime)
        # COMPUTE DISTANCES
        # break_distance = speed^2/2acceleration
        self._breakingDistance = abs(self._speed**2 / (
            2 * self._maxDeaceleration
        ))
        self.updateAcceleration()
        self.updateSpeed()
        self.updateDistance()
        # CHECK IF REACHED
        # reached next station:
        while self._distanceMovedStation > self._distanceToStation:
            # reached destination:
            if not self._path:
                self._atStation = self._currentConnection.station_end
                self._isMoving = False
                break
            self.updateConnection()
            self._distanceToStation = self._currentConnection.distance
            self._distanceMovedStation -= self._distanceToStation
    
    def stop_in(self, station):
        # to stop the last process
        # soft braking system
        self.state = CarriersStates.STOPPING
        self._acceleration = self._maxDeaceleration
        while self._distanceLeftDestination > 0:
            yield self._env.timeout(self._tickTime)
            self.updateSpeed()
            self.updateDistance()
        self._acceleration = 0
        self._distanceToDestination = 0
        self._distanceLeftDestination = 0
        self._distanceMovedStation = 0
        self._movingTo = ""
        self._movingFrom = ""
        self._distanceMoved = 0
        self._atStation = station
        self._passengers = []
        yield self._env.process(self.idle(self._atStation.loader))

    def printDistance(self,file,tick):
        with open(os.path.join(dirname, "../others/plotters/data/"+file), 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = f # Change the standard output to the file we created.
            while True:
                print(f'{self.total_distance:.3f}')
                yield self._env.timeout(tick)
            sys.stdout = original_stdout # Reset the standard output to its original value

    def printSpeed(self,tick):
        while True:
            print(f'{self._distanceLeftDestination:.3f}')
            yield self._env.timeout(tick)

    def printEvents(self):
        preState = CarriersStates.UNUSED
        while True:
            if self.state != preState:
                preState = self.state
                print(f'{self._env.now}: carrier [{self._uid}] {self.state.name},')
                if self.state == CarriersStates.MOVING:
                    print(f'\t moving from {self._movingFrom} to {self._movingTo},')
                elif self.state == CarriersStates.IDLE:
                    print(f'\t in {self._atStation.name}')
                elif self.state == CarriersStates.LOADING:
                    print(f'\t to {self._destination}')
                elif self.state == CarriersStates.STOPPING:
                    print(f'\t in {self._atStation.name}')
                print()
            yield self._env.timeout(1)

    def printTime(self, tick):
        while True:
            print(f't:{self._env.now}')
            yield self._env.timeout(tick)


    def getUID(self):
        return self._uid


c = Carrier("1", Stations["Lyngby"], 1, Stations, Connections, env)
# # c2 = Carrier("2", Stations["Lyngby"], 1, Stations, Connections, env)
env.process(c.deploy())
# # # env.process(c2.deploy())

#env.process(c.printEvents())
env.process(c.printDistance('distances_train.txt',2))
#env.process(c.printSpeed(2))
env.run(until=300)