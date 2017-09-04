import threading
import time
from routingValve import RoutingValve

def releaseLock(lock):
	lock.release();


class EVOPROG_VALVE_I(RoutingValve):
	
	def __init__(self, params):
		"""constructor"""
		self.i2cAddress = params['i2c_address'];
		self.actualPosition = 0;
		self.movingLock = threading.Lock();

	def moveToPosition(self, communications, position):
		"""
			must send instructions to the machine to move this valve to the position "position",
			the command must be sended throught the communications object,
			communications object has the next api:
				*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
				*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
				*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
				*) void synchronize() -- synchronize with the machine;
		"""
		if (position != self.actualPosition) :
			if (position == 0) :
				self.closeValve(communications);
			else :
				self.movingLock.acquire();
				positionsMove = abs(self.actualPosition - position);
			
				communications.sendString("M " + str(self.i2cAddress) + " " + str(position));
				
				timer = threading.Timer(.400 * positionsMove, releaseLock , kwargs = {"lock" : self.movingLock});
				timer.start();
				
				self.actualPosition = position;
	
	def closeValve(self, communications):
		"""
			must send instructions to the machine to close this valve to position "position",
			the command must be sended throught the communications object,
			communications object has the next api:
				*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
				*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
				*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
				*) void synchronize() -- synchronize with the machine;
		"""
		self.movingLock.acquire();
		
		communications.sendString("H " + str(self.i2cAddress));
		
		timer = threading.Timer(3, releaseLock , kwargs = {"lock" : self.movingLock});
		timer.start();
		
		self.actualPosition = 0;