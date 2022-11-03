from time import sleep

class Train:

	
	""" README
		
		Acceleration and deacceleration function uses sleep, so not to instantly 
		accelerate to min/max speed. This needs to be changed to follow some sort
		of tick

		All functions return their related value, makes it easier for testing
		purposes
	"""

	#Amount of passengers on train
	_passengers = 0

	#Speed of train
	_speed = 0

	#Max speed of train
	_maxSpeed = 120

	#Acceleration of train
	_acceleration = 1.3
	_decceleration = 1.2

	#0 when not at a station otherwise station
	_atStation = 0

	#Is the train moving
	_moving = False

	#0 when at a station otherwise station
	_movingTo = 0
	_movingFrom = 0

	#Initialisation of the train
	def __init__(self, station):
		self._atStation = station


	def atStation(self):
		return self._atStation

	def moving(self):
		return self._moving

	def arriveAt(self,station):
		self._atStation = station
		self._moving = False
		return self._atStation
	
	def moveTo(self,station):
		self._movingFrom = self._atStation
		self._movingTo = station
		self._atStation = 0
		self._moving = True
		self.accelerate()
		return self._movingTo

	def goingFromTo(self):
		return (self._movingFrom,self._movingTo)

	def passengerNumber(self):
		return self._passengers

	def boardPassengers(self,passengers):
		self._passengers += passengers
		return self._passengers

	def disembarkPassengers(self,passengers):
		self._passengers -= passengers
		return self._passengers

	def availablePassengerSpace(self):
		return 700 - self._passengers

	def maxPassengers(self):
		return 700

	def speed(self):
		return self._speed

	def accelerate(self):
		while self._speed < 120:
			self._speed = self._speed + self._acceleration
			#sleep(0.1)
		return self._speed

	def decelerate(self):
		while self._speed > 1:
			self._speed = self._speed - self._decceleration
			#sleep(0.1)
		self._speed = 0
		return self._speed

	def printInformation(self):
		print(f"passengers: {self._passengers}")
		print(f"speed: {self._speed}")
		print(f"atStation: {self._atStation}")
		print(f"moving: {self._moving}")
		print(f"movingTo: {self._movingTo}")
		print(f"movingFrom: {self._movingFrom}")
		print(f"availablePassengerSpace: {self.availablePassengerSpace()}")

# train = Train('Central Station')
# train.printInformation()
# print()
# train.boardPassengers(350)
# train.disembarkPassengers(50)
# train.moveTo('Nørreport')
# train.printInformation()
# train.decelerate()
# train.arriveAt('Nørreport')
# print()
# train.printInformation()