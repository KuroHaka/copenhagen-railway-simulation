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