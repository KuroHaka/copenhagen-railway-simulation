from Simulation import Simulation
import sys

from Person import Person
from datetime import datetime, timedelta

def main():
    
    Person.create_passengers(["Lyngby","København H"], {"start": datetime.now(), "end": datetime.now()+timedelta(hours=9)}, 100)
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    weight = 1
    tickLength = 60

    sim = Simulation()

    if (animation):
        sim.run_simulation_with_animation(100, 40)
    else:
        sim.run_simulation(100, 30)
    return

if __name__ == "__main__":
    main()
