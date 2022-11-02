from .Entity import Entity
from abc import abstractproperty

class Moving(Entity):
    @abstractproperty
    def position_x(self):
        pass

    @abstractproperty
    def position_y(self):
        pass

    def display_element(self):
        self.image

class Carrier(Moving):
    pass

class Train(Moving):
    pass