from Simulation import Simulation
import sys

def main():
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'

    sim = Simulation()

    if (animation):
        sim.run_simulation_with_animation(100, 40)
    else:
        sim.run_simulation(100, 30)
    return

if __name__ == "__main__":
    main()
