from flow_core import requires_repo, _procParamBool, _transBool
from gitflow.flow_documenter import formatValuePair, indentText
from gitflow.flow_config import ConfigManager
import pprint


class BaseCondition():
    PASS = 1
    CRITICAL_FAIL = 2
    WARNING = 3

    PARAM_VALID = 'valid'
    PARAM_CRITICAL = 'critical'

    def __init__(self, params):
        # for conditions, the parameters are optional.  If
        # an option is not entered, its defaulted to TRUE
        self.valid = _procParamBool(params, self.PARAM_VALID, True)
        self.critical = _procParamBool(params, self.PARAM_CRITICAL, True)

    def checkCondition(self, args):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        str_list = [formatValuePair(indentText(4) + "Condition", self.__class__.__name__) + "\n",
                    formatValuePair(indentText(5) + "valid Check", _transBool(self.valid)) + "\n",
                    formatValuePair(indentText(5) + "critical Check", _transBool(self.critical)) + "\n"]

        return ''.join(str_list)


class condBranchExist(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + _transBool(self.valid))
        print("  critical Check: " + _transBool(self.critical))
        print("  class Name: " + self.__class__.__name__)


class condIsClean(BaseCondition):
    @requires_repo
    def checkCondition(self, args):
        """
        Returns whether or not the current working directory contains
        uncommitted changes.
        """
        print("go")
        config = ConfigManager()
        pprint.pprint(config)
        print("  valid Check: " + _transBool(self.valid))
        print("  critical Check: " + _transBool(self.critical))
        print("  class Name: " + self.__class__.__name__)
        return config.repo.is_dirty()


class condPushRemote(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + _transBool(self.valid))
        print("  critical Check: " + _transBool(self.critical))
        print("  class Name: " + self.__class__.__name__)


class condIsNextMaster(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + _transBool(self.valid))
        print("  critical Check: " + _transBool(self.critical))
        print("  class Name: " + self.__class__.__name__)


class condDefault(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + _transBool(self.valid))
        print("  critical Check: " + _transBool(self.critical))
        print("  class Name: " + self.__class__.__name__)


class ConditionFactory():
    @staticmethod
    def buildClass(condition, params):
        constructor = globals()[condition]
        instance = constructor(params)
        return instance
