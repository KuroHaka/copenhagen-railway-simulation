import sys
from Simulation import Simulation
from datetime import datetime, timedelta

def main():

    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'

    sim = Simulation()

    if (animation):
        sim.run_carriers_simulation_animation(1*60*60,10, datetime(2022,9,24))
    else:
        sim.run_carriers_simulation(1*60*60, datetime(2022,9,24))
    return

if __name__ == "__main__":
    main()
