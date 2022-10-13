import simpy
import pygame
from abc import ABC, abstractproperty


class Entity(ABC):
    @abstractproperty
    def image(self):
        pass

    def get_figure(self):
        return self.image

class Car(Entity):
    image = 'Gene youre awesome'

class Station(Entity):
    image = 'Gene is a genius'

class Person(Entity):
    image = 'Gene is so hot'


def main():
    print("Starting simulation...")
    lamborgini = Car()
    print(lamborgini.get_figure())
    nørrebro = Station()
    print(nørrebro.get_figure())
    gene = Person()
    print(gene.get_figure())
    return


if __name__ == "__main__":
    main()