
class CommunicationsTerminal():
	def __init__(self, stringList):
		self.stringList = stringList;
		self.actualPosition = 0;

	"""
		*) nbytessend sendString(string) -- send the string to the machine, return the bytes sended;
		*) string receiveString() -- receive and returns a string from the machine (stops when \n is received), can block;
		*) string readUntil(endCharacter) -- returns a string received from the machine, stops when the endCharacter arrives;
		*) void synchronize() -- synchronize with the machine;
	"""
	def sendString(self, string):
		print string;
	
	def receiveString(self):
		stringsNumber = len(self.stringList);
		if (stringsNumber == 0):
			return "";
		else:
			if (self.actualPosition >= stringsNumber) :
				self.actualPosition = 0;
				
			strToReturn = self.stringList[self.actualPosition];
			self.actualPosition += 1;
			
			return strToReturn;
	
	def readUntil(self, endCharacter):
		return "";
	
	def synchronize(self):
		return 0;