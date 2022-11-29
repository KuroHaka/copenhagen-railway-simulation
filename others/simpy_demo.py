import simpy

# from train_simulation.Railway import Station, Stations, Lines, Connections, Connection
TICKTIME = 40
stations = {}

class Carrier:
    def __init__(self, uid, env):
        self.uid = uid
        self.moving = False
        self.env: simpy.Environment = env
        self._passengers = []
        self._loading_duration = 20
        self._departure_time = 0
        self._stations = []
        self._from_station = ""
        self._to_station = ""
        self._in_station = ""
        self._destination = ""
        self._distance_moved = 0

    def idle(self, loading):
        print(self.uid, "idle")
        request = loading.request()
        yield request
        # load passengers
        print(self.uid, "loading")
        self._passengers = [1,2,3,4]
        if self._in_station == 'a':
            self._destination = 'b'
        else:
            self._destination = 'a'
        yield self.env.timeout(self._loading_duration)

        # compute path from algorithms
        self._stations = [self._destination]
        loading.release(request)

        self.env.process(self.running())

    def running(self):
        print(self.uid, "departed")
        self.moving = True
        self._departure_time = self.env.now
        for station in self._stations:
            self.move_to(station)
            # compute position
            for i in range(0, 100, 30):
                print(self.uid, "position x y", i)
                yield self.env.timeout(TICKTIME)

        self.unload()

    def unload(self):
        print(self.uid, "end trip:", self.env.now - self._departure_time)

        # compute passengers commute time
        self.passenger = []
        stations[self._destination].enqueue(self)

    def move_to(self, station_name):
        self._to_station = station_name
        self._from_station = self._in_station
        self._in_station = ""
        # self._distance_moved = TODO

    def stop_in(self, station_name):
        self._to_station = ""
        self._from_station = ""
        self._distance_moved = 0
        self._in_station = station_name


class Station:
    def __init__(self, name, env, capacity, carriers):
        self.name = name
        self.passengers = []
        self.env = env
        self.loader = simpy.Resource(self.env, capacity=capacity)
        for c in carriers:
            c.stop_in(self.name)
            env.process(c.idle(self.loader))
    
    def enqueue(self, carrier):
        carrier.stop_in(self.name)
        self.env.process(carrier.idle(self.loader))


env = simpy.Environment()
carriers = {}
for i in range(10):
    carriers["c" + str(i).zfill(4)] = Carrier("c" + str(i).zfill(5), env)
c1 = [carriers['c0001'],carriers['c0002'],carriers['c0003'],carriers['c0004']]
c2 = [carriers['c0000'],carriers['c0005'],carriers['c0006'],carriers['c0007']]

stations["a"] = Station("a",env,1,c1)
stations["b"] = Station("b",env,1,c2)

env.run(until=30 * 60)
