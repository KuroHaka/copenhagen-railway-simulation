import simpy
import pygame
from abc import ABC, abstractproperty



class Train(Moving):
    image = 'Gene youre awesome'
    position_x = 0
    position_y = 0


class Station(Moving):
    image = 'Gene is a genius'
    position_x = 0
    position_y = 0

class Person(Entity):
    image = 'Gene is so hot'
    position_x = 0

class Railway(Entity):
    image = 'Gene is '
    position_x = 0


def main():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([1000, 700])
    return


if __name__ == "__main__":
    main()