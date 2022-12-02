from Simulation import Simulation, CarrierSimulation
import sys

from Person import Person, create_passengers
from datetime import datetime, timedelta

from Algorithms import Algorithms
from Person import create_passengers

def main():

    # Carrier maxspeed = 80 km/h, 40 km/h

    #animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    tickLength = 30

    # print("Creating passegners")
    # create_passengers(['København H', 'Svanemøllen'], {"start": datetime(2018, 10, 22, 6, 0, 0), "end": datetime(2018, 10, 22, 12, 0, 0)}, 12500)

    print("Creating carrier simulation")
    simCarrier = CarrierSimulation(300,['København H','Lyngby'],datetime(2018, 10, 22, 0, 0, 0))

    print("Creating train simulation")
    simTrain = Simulation(52,datetime(2018, 10, 22, 0, 0, 0))

    # print(len(sim.trains))
    # print(sim.passerngersToGenerate[0])

    #create_passengers(critical_stations, time, n_passengers)

    # algo = sim.algo
    # x = algo.get_path_trains('Charlottenlund','Buddinge')
    # print(x)

    # if (animation):
    #     sim.run_simulation_with_animation(200, 40)
    # else:
    #     sim.run_simulation(3000, 30)
    
    print("Created simulations")
    print("Running simulations")
    simCarrier.run_simulation(3000, tickLength)
    print("Carrier simulation done")
    simTrain.run_simulation(3000, tickLength)
    print("Trains simulation done")
    print()
    print()

    
    # Average travling time
    print("Calculating average travel time")
    print()
    print("Carriers:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for i in simCarrier.allPassengersGenerated:
        if i.travel_time:
            totalTravelTime += i.travel_time
            totalPassengersArrived += 1
        else:
            totalPassengersNotArrived += 1
    
    print(totalTravelTime.total_seconds()/totalPassengersArrived/60)
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")
    print()

    print("Trains:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for i in simTrain.allPassengersGenerated:
        if i.travel_time:
            totalTravelTime += i.travel_time
            totalPassengersArrived += 1
        else:
            totalPassengersNotArrived += 1
    
    print(totalTravelTime.total_seconds()/totalPassengersArrived/60)
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")



    # average travling time based on distance traveled
    print("Calculating average travel time per distance traveled NOT DONE")
    print()
    print("Carriers:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for i in simCarrier.allPassengersGenerated:
        if i.travel_time:
            totalTravelTime += i.travel_time
            totalPassengersArrived += 1
        else:
            totalPassengersNotArrived += 1
    
    print(totalTravelTime.total_seconds()/totalPassengersArrived/60)
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")
    print()

    print("Trains:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for i in simTrain.allPassengersGenerated:
        if i.travel_time:
            totalTravelTime += i.travel_time
            totalPassengersArrived += 1
        else:
            totalPassengersNotArrived += 1
    
    print(totalTravelTime.total_seconds()/totalPassengersArrived/60)
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")



    # average travling time based on when travel started

    # average time spent NOT traveling

    # average travling time based on passengerspace on carriers

    # speed of train/carrier based on distance to station

    # speed of which carriers are better than trains


    # total time spent accelerating for all trains/carriers (calculate how much energy it takes to reach "max_speed")


    return


if __name__ == "__main__":
    main()
