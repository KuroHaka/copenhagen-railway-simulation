import sys
from Simulation import Simulation
from datetime import datetime, timedelta

def main():

    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'

    sim = Simulation()

    if (animation):
        sim.run_carriers_simulation_animation(1000, 10)
    else:
        sim.run_carriers_simulation(24*60*60)
    return

if __name__ == "__main__":
    main()
