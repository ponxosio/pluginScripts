import datetime
import threading
import time
from mixer import Mixer;

class EVOPROG_MIXER(Mixer):
	lastId = 0;
	idMaster = 0;

	def __init__(self, params):
		"""constructor"""
		self.controllerId = params["controller_id"];
		
		positionStr = params["fan_positions"];
		self.positions = positionStr.split(",");
		
		self.actualSpeed = 0;
		self.lockWorking = threading.Lock();
		
		self.id = EVOPROG_MIXER.lastId;
		EVOPROG_MIXER.lastId += 1;
		
		
	def setNormalIntensity(self, communications) :
		for pos in self.positions :
			communications.sendString("FAN " + str(self.controllerId) + " " + str(pos) + " " + str(self.actualSpeed));
		
		self.lockWorking.release();

	def mix(self, communications, intensity):
		"""must send instructions to stir the liquid at the given real number "intensity" Hz, 
		communication with the machine must be done via communications object
		ommunications object has the next api:
				*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
				*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
				*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
				*) void synch() -- synchronize with the machine, not always necesary, only for protocols compatibles;
		"""
		if (self.actualSpeed != intensity) :
			if (intensity == 0) :
				self.stopMixing(communications);
			else :
				if (self.id == EVOPROG_MIXER.idMaster) :
					self.lockWorking.acquire();
					
					if (self.actualSpeed == 0 and intensity < 40) :
						for pos in self.positions :
							communications.sendString("FAN " + str(self.controllerId) + " " + str(pos) + " 40");
						
						timer = threading.Timer(3, self.setNormalIntensity , kwargs = {"communications" : communications});
						timer.start();
					else :
						for pos in self.positions :
							communications.sendString("FAN " + str(self.controllerId) + " " + str(pos) + " " + str(intensity));
						
						self.lockWorking.release();					
				self.actualSpeed = intensity;

	def stopMixing(self, communications):
		"""must send instructions to stop the actuator, 
		communication with the machine must be done via communications object
		ommunications object has the next api:
				*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
				*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
				*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
				*) void synch() -- synchronize with the machine, not always necesary, only for protocols compatibles;
		"""
		if (self.actualSpeed != 0) :
			if (self.id == EVOPROG_MIXER.idMaster) :
				self.lockWorking.acquire();
				
				for pos in self.positions :
					communications.sendString("FAN " + str(self.controllerId) + " " + str(pos) + " 0");

				self.lockWorking.release();
				
			self.actualSpeed = 0;