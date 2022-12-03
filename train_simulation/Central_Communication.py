from Simulation import Simulation, CarrierSimulation
import sys

from Person import Person, create_passengers
from datetime import datetime, timedelta

from Algorithms import Algorithms
from Person import create_passengers

def main():

    # Carrier maxspeed = 80 km/h, 40 km/h

    #animation = len(sys.argv)>1 and sys.argv[1] == 'animation'
    simulationLength = 5000
    tickLength = 30
    numberCarriers = 5000
    numberPassengers = 125000



    print("Environment:")
    print(f"Tick length (seconds): {tickLength}")
    print(f"Amount of ticks: {simulationLength} (meaning the simulation will run for {(simulationLength*tickLength)/60/60} hours)")
    print(f"Amount of passengers generated: {numberPassengers}")
    print(f"Amount of Carriers: {numberCarriers}")
    print(f"Amount of people carriers can carry: {5}")

    print()
    print()

    print("Creating passegners")
    create_passengers(['København H', 'Svanemøllen'],datetime(2018, 10, 22, 6, 0, 0), datetime(2018, 10, 22, 23, 59, 59), numberPassengers)

    print("Creating carrier simulation")
    simCarrier = CarrierSimulation(numberCarriers,['København H','Lyngby'],datetime(2018, 10, 22, 0, 0, 0))

    print("Creating train simulation")
    simTrain = Simulation(52,datetime(2018, 10, 22, 0, 0, 0))
    print()

    
    print("Created simulations")
    print("Running simulations")
    print()
    simCarrier.run_simulation(simulationLength, tickLength)
    print("Carrier simulation done")
    simTrain.run_simulation(simulationLength, tickLength)
    print("Trains simulation done")
    print()
    print()

    
    # Average travling time
    print("Calculating average travel time")

    print("Carriers:")
    waitTimes = []
    totalPassengersNotArrived = 0
    for passenger in simCarrier.allPassengersGenerated:
        if passenger.travel_time:
            waitTimes.append(passenger.travel_time.total_seconds()/60)
        else:
            totalPassengersNotArrived += 1
    
    print(sum(waitTimes)/len(waitTimes))
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")
    print()

    print("Trains:")
    waitTimes = []
    totalPassengersNotArrived = 0
    for passenger in simTrain.allPassengersGenerated:
        if passenger.travel_time:
            waitTimes.append(passenger.travel_time.total_seconds()/60)
        else:
            totalPassengersNotArrived += 1
    
    print(sum(waitTimes)/len(waitTimes))
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")
    print()
    print()










    # Average waiting time
    print("Calculating average waiting time")

    print("Carriers:")
    waitTimes = []
    totalPassengersNotArrived = 0
    for passenger in simCarrier.allPassengersGenerated:
        if passenger.travel_time:
            waitTimes.append(passenger.timeSpentWaiting.total_seconds()/60)
        else:
            totalPassengersNotArrived += 1
    
    print(sum(waitTimes)/len(waitTimes))
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")
    print()

    print("Trains:")
    waitTimes = []
    totalPassengersNotArrived = 0
    for passenger in simTrain.allPassengersGenerated:
        if passenger.travel_time:
            waitTimes.append(passenger.timeSpentWaiting.total_seconds()/60)
        else:
            totalPassengersNotArrived += 1
    
    print(sum(waitTimes)/len(waitTimes))
    print(f"Number of passengers not arrived {totalPassengersNotArrived}")
    print()
    print()










    #Average travling time based on distance traveled
    print("Calculating average travel time per distance traveled")

    carrier1km = []
    carrier2km = []
    carrier5km = []
    carrier10km = []
    carrier20km = []
    carrierMaxkm = []


    print("Carriers:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for passenger in simCarrier.allPassengersGenerated:
        passengerDistanceTraveled = 0
        if passenger.travel_time:
            path = passenger.path
            for i in range(len(path)-1):
                passengerDistanceTraveled += simCarrier.connections[(path[i],path[i+1])].distance
            if passengerDistanceTraveled < 1000:
                carrier1km.append(passenger.travel_time.total_seconds()/60)

            if 1000 <= passengerDistanceTraveled < 2000:
                carrier2km.append(passenger.travel_time.total_seconds()/60)

            if 2000 <= passengerDistanceTraveled < 5000:
                carrier5km.append(passenger.travel_time.total_seconds()/60)

            if 5000 <= passengerDistanceTraveled < 10000:
                carrier10km.append(passenger.travel_time.total_seconds()/60)

            if 10000 <= passengerDistanceTraveled < 20000:
                carrier20km.append(passenger.travel_time.total_seconds()/60)

            if 20000 <= passengerDistanceTraveled:
                carrierMaxkm.append(passenger.travel_time.total_seconds()/60)

        else:
            totalPassengersNotArrived += 1
    
    print(f"Average under 1km {sum(carrier1km)/len(carrier1km)}, amount traveled this distance {len(carrier1km)}")
    print(f"Average under 2km, but above 1km {sum(carrier2km)/len(carrier2km)}, amount traveled this distance {len(carrier2km)}")
    print(f"Average under 5km, but above 2km {sum(carrier5km)/len(carrier5km)}, amount traveled this distance {len(carrier5km)}")
    print(f"Average under 10km, but above 5km {sum(carrier10km)/len(carrier10km)}, amount traveled this distance {len(carrier10km)}")
    print(f"Average under 20km, but above 10km {sum(carrier20km)/len(carrier20km)}, amount traveled this distance {len(carrier20km)}")
    print(f"Average more than 20km {sum(carrierMaxkm)/len(carrierMaxkm)}, amount traveled this distance {len(carrierMaxkm)}")
    print()

    train1km = []
    train2km = []
    train5km = []
    train10km = []
    train20km = []
    trainMaxkm = []

    print("Trains:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for passenger in simTrain.allPassengersGenerated:
        passengerDistanceTraveled = 0
        if passenger.travel_time:
            path = passenger.path
            actualPath = []
            for line in range(len(path)):
                if line == 0:
                    actualPath += path[line]['path']
                else:
                    actualPath += path[line]['path'][1:]
                for i in range(len(actualPath)-1):
                    passengerDistanceTraveled += simTrain.connections[(actualPath[i],actualPath[i+1])].distance
            if passengerDistanceTraveled < 1000:
                train1km.append(passenger.travel_time.total_seconds()/60)

            if 1000 <= passengerDistanceTraveled < 2000:
                train2km.append(passenger.travel_time.total_seconds()/60)

            if 2000 <= passengerDistanceTraveled < 5000:
                train5km.append(passenger.travel_time.total_seconds()/60)

            if 5000 <= passengerDistanceTraveled < 10000:
                train10km.append(passenger.travel_time.total_seconds()/60)

            if 10000 <= passengerDistanceTraveled < 20000:
                train20km.append(passenger.travel_time.total_seconds()/60)

            if 20000 <= passengerDistanceTraveled:
                trainMaxkm.append(passenger.travel_time.total_seconds()/60)

        else:
            totalPassengersNotArrived += 1

    print(f"Average under 1km {sum(train1km)/len(train1km)}, amount traveled this distance {len(train1km)}")
    print(f"Average under 2km, but above 1km {sum(train2km)/len(train2km)}, amount traveled this distance {len(train2km)}")
    print(f"Average under 5km, but above 2km {sum(train5km)/len(train5km)}, amount traveled this distance {len(train5km)}")
    print(f"Average under 10km, but above 5km {sum(train10km)/len(train10km)}, amount traveled this distance {len(train10km)}")
    print(f"Average under 20km, but above 10km {sum(train20km)/len(train20km)}, amount traveled this distance {len(train20km)}")
    print(f"Average more than 20km {sum(trainMaxkm)/len(trainMaxkm)}, amount traveled this distance {len(trainMaxkm)}")
    print()
    print()










    #Average travling time based on distance traveled (minus time spent waiting)
    print("Calculating average travel time per distance traveled (minus time spent waiting)")


    carrier1km = []
    carrier2km = []
    carrier5km = []
    carrier10km = []
    carrier20km = []
    carrierMaxkm = []


    print("Carriers:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for passenger in simCarrier.allPassengersGenerated:
        passengerDistanceTraveled = 0
        if passenger.travel_time:
            path = passenger.path
            for i in range(len(path)-1):
                passengerDistanceTraveled += simCarrier.connections[(path[i],path[i+1])].distance
            if passengerDistanceTraveled < 1000:
                carrier1km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 1000 <= passengerDistanceTraveled < 2000:
                carrier2km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 2000 <= passengerDistanceTraveled < 5000:
                carrier5km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 5000 <= passengerDistanceTraveled < 10000:
                carrier10km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 10000 <= passengerDistanceTraveled < 20000:
                carrier20km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 20000 <= passengerDistanceTraveled:
                carrierMaxkm.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

        else:
            totalPassengersNotArrived += 1
    
    print(f"Average under 1km {sum(carrier1km)/len(carrier1km)}, amount traveled this distance {len(carrier1km)}")
    print(f"Average under 2km, but above 1km {sum(carrier2km)/len(carrier2km)}, amount traveled this distance {len(carrier2km)}")
    print(f"Average under 5km, but above 2km {sum(carrier5km)/len(carrier5km)}, amount traveled this distance {len(carrier5km)}")
    print(f"Average under 10km, but above 5km {sum(carrier10km)/len(carrier10km)}, amount traveled this distance {len(carrier10km)}")
    print(f"Average under 20km, but above 10km {sum(carrier20km)/len(carrier20km)}, amount traveled this distance {len(carrier20km)}")
    print(f"Average more than 20km {sum(carrierMaxkm)/len(carrierMaxkm)}, amount traveled this distance {len(carrierMaxkm)}")
    print()

    train1km = []
    train2km = []
    train5km = []
    train10km = []
    train20km = []
    trainMaxkm = []

    print("Trains:")
    totalTravelTime = timedelta(0)
    totalPassengersArrived = 0
    totalPassengersNotArrived = 0
    for passenger in simTrain.allPassengersGenerated:
        passengerDistanceTraveled = 0
        if passenger.travel_time:
            path = passenger.path
            actualPath = []
            for line in range(len(path)):
                if line == 0:
                    actualPath += path[line]['path']
                else:
                    actualPath += path[line]['path'][1:]
                for i in range(len(actualPath)-1):
                    passengerDistanceTraveled += simTrain.connections[(actualPath[i],actualPath[i+1])].distance
            if passengerDistanceTraveled < 1000:
                train1km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 1000 <= passengerDistanceTraveled < 2000:
                train2km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 2000 <= passengerDistanceTraveled < 5000:
                train5km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 5000 <= passengerDistanceTraveled < 10000:
                train10km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 10000 <= passengerDistanceTraveled < 20000:
                train20km.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

            if 20000 <= passengerDistanceTraveled:
                trainMaxkm.append((passenger.travel_time-passenger.timeSpentWaiting).total_seconds()/60)

        else:
            totalPassengersNotArrived += 1

    print(f"Average under 1km {sum(train1km)/len(train1km)}, amount traveled this distance {len(train1km)}")
    print(f"Average under 2km, but above 1km {sum(train2km)/len(train2km)}, amount traveled this distance {len(train2km)}")
    print(f"Average under 5km, but above 2km {sum(train5km)/len(train5km)}, amount traveled this distance {len(train5km)}")
    print(f"Average under 10km, but above 5km {sum(train10km)/len(train10km)}, amount traveled this distance {len(train10km)}")
    print(f"Average under 20km, but above 10km {sum(train20km)/len(train20km)}, amount traveled this distance {len(train20km)}")
    print(f"Average more than 20km {sum(trainMaxkm)/len(trainMaxkm)}, amount traveled this distance {len(trainMaxkm)}")
    print()
    print()










    #Average travling time based on when travel started
    print("Calculating average traveling time based on when travel started")

    print("Carriers:")

    beforeFirstRushHour = []
    firstRushHour = []
    afterFirstRushHour = []
    secondRushHour = []
    afterSecondRushHour = []
    end_time = simCarrier.start_time + timedelta(seconds=simCarrier.cumulativeTick)

    for passenger in simCarrier.allPassengersGenerated:
        if passenger.start_time.hour < 7:
            beforeFirstRushHour.append(passenger.travel_time.total_seconds()/60)
        if 7 <= passenger.start_time.hour < 11:
            firstRushHour.append(passenger.travel_time.total_seconds()/60)
        if 9 <= passenger.start_time.hour < 13:
            afterFirstRushHour.append(passenger.travel_time.total_seconds()/60)
        if 13 <= passenger.start_time.hour < 18:
            secondRushHour.append(passenger.travel_time.total_seconds()/60)
        if 18 <= passenger.start_time.hour:
            afterSecondRushHour.append(passenger.travel_time.total_seconds()/60)

    print(f"Average before first rush hour {sum(beforeFirstRushHour)/(len(beforeFirstRushHour) or 1)}, amount started their travel in this timeframe {len(beforeFirstRushHour)}")
    print(f"Average at first rush hour {sum(firstRushHour)/(len(firstRushHour) or 1)}, amount started their travel in this timeframe {len(firstRushHour)}")
    print(f"Average after first rush hour {sum(afterFirstRushHour)/(len(afterFirstRushHour) or 1)}, amount started their travel in this timeframe {len(afterFirstRushHour)}")
    print(f"Average at second rush hour {sum(secondRushHour)/(len(secondRushHour) or 1)}, amount started their travel in this timeframe {len(secondRushHour)}")
    print(f"Average after first rush hour {sum(afterSecondRushHour)/(len(afterSecondRushHour) or 1)}, amount started their travel in this timeframe {len(afterSecondRushHour)}")
    print()

    print("Trains:")

    beforeFirstRushHour = []
    firstRushHour = []
    afterFirstRushHour = []
    secondRushHour = []
    afterSecondRushHour = []

    for passenger in simTrain.allPassengersGenerated:
        if passenger.start_time.hour < 7:
            beforeFirstRushHour.append(passenger.travel_time.total_seconds()/60)
        if 7 <= passenger.start_time.hour < 11:
            firstRushHour.append(passenger.travel_time.total_seconds()/60)
        if 9 <= passenger.start_time.hour < 13:
            afterFirstRushHour.append(passenger.travel_time.total_seconds()/60)
        if 13 <= passenger.start_time.hour < 18:
            secondRushHour.append(passenger.travel_time.total_seconds()/60)
        if 18 <= passenger.start_time.hour:
            afterSecondRushHour.append(passenger.travel_time.total_seconds()/60)
    
    print(f"Average before first rush hour {sum(beforeFirstRushHour)/(len(beforeFirstRushHour) or 1)}, amount started their travel in this timeframe {len(beforeFirstRushHour)}")
    print(f"Average at first rush hour {sum(firstRushHour)/(len(firstRushHour) or 1)}, amount started their travel in this timeframe {len(firstRushHour)}")
    print(f"Average after first rush hour {sum(afterFirstRushHour)/(len(afterFirstRushHour) or 1)}, amount started their travel in this timeframe {len(afterFirstRushHour)}")
    print(f"Average at second rush hour {sum(secondRushHour)/(len(secondRushHour) or 1)}, amount started their travel in this timeframe {len(secondRushHour)}")
    print(f"Average after first rush hour {sum(afterSecondRushHour)/(len(afterSecondRushHour) or 1)}, amount started their travel in this timeframe {len(afterSecondRushHour)}")
    print()
    print()










    # total time spent accelerating for all trains/carriers (calculate how much energy it takes to reach "max_speed")
    print("Calculating the energy used to accelerate for trains/carriers")

    print("Carriers:")

    totalEnergySpent = 0
    for carrier in simCarrier.carriers.values():
        totalEnergySpent += 0.55*carrier._maxPassengers*(carrier._metersDriven/1000)

    #We assume 0,55 MJ energy per passenger-kilometre
    #https://en.wikipedia.org/wiki/ULTra_(rapid_transit) , Description->Vehicles: "energy requirement of 0.55 MJ per passenger-kilometre"
    print(f"Total energy spent among all carriers: {totalEnergySpent}")
    print(f"Average energy spent per carrier: {totalEnergySpent/len(simCarrier.carriers)}")
    print()


    print("Trains:")
    totalEnergySpent = 0
    for train in simTrain.trains.values():
        totalEnergySpent += 0.09*340*(train._metersDriven/1000)

    #We assume 0,09 MJ energy per passenger-kilometre (sædekilometer in danish, aka seat-kilometre, which is why I use the amount of seats and not the max amount of passengers)
    #https://ens.dk/sites/ens.dk/files/Analyser/energiforbrug_for_tog_og_fly.pdf , section 2.10: "0,07 - 0,09 MJ el pr. sædekilomete"
    
    print(f"Total energy spent among all trains: {totalEnergySpent}")
    print(f"Average energy spent per train: {totalEnergySpent/len(simTrain.trains)}")
    print()
    print()


    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print("====================NEW SIMULATION RUN====================")
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()


    # total time spent accelerating for all trains/carriers (calculate how much energy it takes to reach "max_speed")


    # average travling time based on passengerspace on carriers

    # speed of train/carrier based on distance to station

    # speed of which carriers are better than trains


    


    return


if __name__ == "__main__":
    main()
