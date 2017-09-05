from temperature import Temperature;

class EVOPROG_HEATER(Temperature):

	def __init__(self, params):
		"""constructor"""
		self.controllerId = params["controller_id"];
		self.actualTemperature = 0;

	def applyTemperature(self, communications, temperature):
		"""must send instructions to change the temperature to the given real number "temperature" in C, 
		communication with the machine must be done via communications object
		ommunications object has the next api:
				*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
				*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
				*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
				*) void synch() -- synchronize with the machine, not always necesary, only for protocols compatibles;
		"""
		degreeTemperature = temperature ;#- 273.15;
		if (degreeTemperature != self.actualTemperature) :
			if (degreeTemperature == 0) :
				self.turnOff(communications);
			else :
				communications.sendString("TEMP " + str(self.controllerId) + " " + str(degreeTemperature));
				if (self.actualTemperature == 0) :
					communications.sendString("reg " + str(self.controllerId));
				self.actualTemperature = degreeTemperature;

	def turnOff(self, communications):
		"""must send instructions to stop the actuator, 
		communication with the machine must be done via communications object
		ommunications object has the next api:
				*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
				*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
				*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
				*) void synch() -- synchronize with the machine, not always necesary, only for protocols compatibles;
		"""
		communications.sendString("regStop " + str(self.controllerId));
		self.actualTemperature = 0;