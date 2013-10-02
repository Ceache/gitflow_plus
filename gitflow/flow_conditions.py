class BaseCondition(object):
    PASS = 1
    CRITICAL_FAIL = 2
    WARNING = 3

    def __init__(self, valid, critical):

        if isinstance(valid, str):
            self.valid = self.to_bool(valid)
        else:
            self.valid = valid

        if isinstance(critical, str):
            self.critical = self.to_bool(critical)
        else:
            self.critical = critical

    def to_bool(self, value):
        valid = {'true': True, 't': True, '1': True,
                 'false': False, 'f': False, '0': False}

        if not isinstance(value, str):
            raise ValueError('invalid literal for boolean. Not a string.')

        lower_value = value.lower()
        print(lower_value)
        if lower_value in valid:
            return valid[lower_value]
        else:
            raise ValueError('invalid literal for boolean: "%s"' % value)

    def checkCondition(self):
        raise NotImplementedError("Should have implemented this")

    def _transBool(self, b):
        print(type(b))
        if b is True:
            return "True"
        else:
            return "False"

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
    def buildClass(condition, valid, critical):
        constructor = globals()[condition]
        instance = constructor(valid, critical)
        return instance
