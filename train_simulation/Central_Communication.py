from Simulation import Simulation
import sys

from Person import Person
from datetime import datetime, timedelta

from Algorithms import Algorithms

def main():
    
    # Person.create_passengers(["Lyngby","København H"], {"start": datetime.now(), "end": datetime.now()+timedelta(hours=9)}, 100)
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    weight = 1
    tickLength = 60

    sim = Simulation()

    # algo = Algorithms(sim.connections,sim.stations,sim.lines)
    # print(algo.get_path('Lyngby','Malmparken').nodes)

    if (animation):
        sim.run_simulation_with_animation(120, 10, output_fig=True)
    else:
        sim.run_simulation(100, 30)
    return

if __name__ == "__main__":
    main()
