

class BaseCondition(object):

	def __init__(self, valid, critical):
		self.valid = valid
		self.critical = critical

	def checkCondition(self):
		raise NotImplementedError( "Should have implemented this" )

	def _transBool(self, b):
		if b:
			return "True"
		else:
			return "False"

class condBranchExist(BaseCondition):
	def checkCondition(self):
		print("valid Check: " + self._transBool(self.valid))
		print("critical Check: " + self._transBool(self.critical))
		print("class Name: " + self.__class__.__name__)

class condIsClean(BaseCondition):
	def checkCondition(self):
		print("valid Check: " + self._transBool(self.valid))
		print("critical Check: " + self._transBool(self.critical))
		print("class Name: " + self.__class__.__name__)

class condPushRemote(BaseCondition):
	def checkCondition(self):
		print("valid Check: " + self._transBool(self.valid))
		print("critical Check: " + self._transBool(self.critical))
		print("class Name: " + self.__class__.__name__)

class condIsNextMaster(BaseCondition):
	def checkCondition(self):
		print("valid Check: " + self._transBool(self.valid))
		print("critical Check: " + self._transBool(self.critical))
		print("class Name: " + self.__class__.__name__)

class condDefault(BaseCondition):
	def checkCondition(self):
		print("valid Check: " + self._transBool(self.valid))
		print("critical Check: " + self._transBool(self.critical))
		print("class Name: " + self.__class__.__name__)

class ConditionFactory():
	def buildClass(self, condition, valid, critical):
		constructor = globals()[condition]
		instance = constructor(valid, critical)
		return instance
