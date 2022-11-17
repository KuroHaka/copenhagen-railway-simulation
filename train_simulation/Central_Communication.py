from Simulation import Simulation
import sys

def main():
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    weight = 1
    tickLength = 60

    sim = Simulation()

    for i in range(240):
        sim.tickPersonGeneration(weight,tickLength)
        sim.tickTrain(tickLength)
        sim.printAllTrainInformation()
    # totalPassengerArrived = 0
    # totalTravelTime = 0
    # travelTimePerLine = 0
    # for person in allPassengersGenerated:
    #     if person.isArrived():
    #         totalPassengerArrived += 1
    #         totalTravelTime += person.getTravelTime()

    # print(f"A total of {totalPassengerArrived} passengers arrived at thier destination")
    # print(f"It took them a total of {totalTravelTime} minutes, that is an average of {totalTravelTime/totalPassengerArrived} per passenger")
    # print(f"Simulation ran for {cumulativeTick/60} minutes")

    # if (animation):
    #     sim.run_simulation_with_animation(100, 40)
    # else:
    #     sim.run_simulation(100, 30)
    # return

if __name__ == "__main__":
    main()
