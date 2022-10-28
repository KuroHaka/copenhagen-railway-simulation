from abc import ABC, abstractproperty
import Station

class Entity(ABC):
    @abstractproperty
    def image(self):
        pass

    def get_figure(self):
        return self.image

class Moving(Entity):
    @abstractproperty
    def position_x(self):
        pass

    @abstractproperty
    def position_y(self):
        pass

    def display_element(self):
        self.image

class Connection():
    def __init__(self, station_a, x, y, passengers):
        self.station_a = station_a
        self.station_b = station_b
        self.distance = distance
