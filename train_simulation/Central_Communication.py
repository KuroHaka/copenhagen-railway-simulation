from Simulation import Simulation
import sys

from Person import Person, create_passengers
from datetime import datetime, timedelta

from Algorithms import Algorithms
from Person import create_passengers

def main():
    
    # Person.create_passengers(["Lyngby","København H"], {"start": datetime.now(), "end": datetime.now()+timedelta(hours=9)}, 100)
    animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    weight = 1
    tickLength = 60

    #create_passengers(['København H', 'Svanemøllen'], {"start": datetime(2018, 10, 22, 0, 0, 0), "end": datetime(2018, 10, 22, 8, 0, 0)}, 500)
    sim = CarrierSimulation(300,['København H','Lyngby'],datetime(2018, 10, 22, 0, 0, 0))
    sim = Simulation(52,['Lyngby'],datetime(2018, 10, 22, 0, 0, 0))

    # print(len(sim.trains))
    # print(sim.passerngersToGenerate[0])

    #create_passengers(critical_stations, time, n_passengers)

    # algo = sim.algo
    # x = algo.get_path_trains('Charlottenlund','Buddinge')
    # print(x)

    if (animation):
        sim.run_simulation_with_animation(200, 40)
    else:
        sim.run_simulation(2000, 30)
    

    # numCar = 0
    # print(len(sim.carriers))
    # for station in sim.stations.values():
    #     print(station.name, len(station.carriers))
    #     numCar += len(station.carriers)
    # print(numCar)

    # print(len(sim.stations['Køge'].carriers))

    totalTravelTime = timedelta(0)
    for i in sim.allPassengersGenerated:
        #print(i.start_station,i.destination,i.isArrived)
        if not i.travel_time:
            print("wtf")
            continue


    totalTravelTime = timedelta(0)
    
    for i in sim.allPassengersGenerated:
        totalTravelTime += i.travel_time
        print(i.travel_time)

    print(totalTravelTime.total_seconds()/len(sim.allPassengersGenerated)/60)

    return


if __name__ == "__main__":
    main()
