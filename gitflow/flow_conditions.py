from flow_core import GitflowCoreCommands


class BaseCondition(GitflowCoreCommands):
    PASS = 1
    CRITICAL_FAIL = 2
    WARNING = 3

    PARAM_VALID = 'valid'
    PARAM_CRITICAL = 'critical'

    def __init__(self, params):
        # for conditions, the parameters are optional.  If
        # an option is not entered, its defaulted to TRUE
        self.valid = self._procParamBool(params, self.PARAM_VALID, True)
        self.critical = self._procParamBool(params, self.PARAM_CRITICAL, True)

    def checkCondition(self):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        str_list = ["        Condition: " + self.__class__.__name__ + "\n",
                    "          valid Check: " + self._transBool(self.valid) + "\n",
                    "          critical Check: " + self._transBool(self.critical) + "\n"]
        return ''.join(str_list)


class condBranchExist(BaseCondition):
    def checkCondition(self):
        print()
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
    @staticmethod
    def buildClass(condition, params):
        constructor = globals()[condition]
        instance = constructor(params)
        return instance
