__author__ = 'LID4EC9'


class GitflowCoreCommands(object):

    def _procParamString(self, inputParamDic, key, default):
        ret = default
        if inputParamDic is not None:
            if inputParamDic.get(key) is not None:
                ret = inputParamDic[key]

        return ret

    def _procParamBool(self, inputParamDic, key, default):
        ret = default
        if inputParamDic.get(key) is not None:
            if isinstance(inputParamDic[key], str):
                ret = self.to_bool(inputParamDic[key])
            else:
                ret = inputParamDic[key]

        return ret

    def to_bool(self, value):
        valid = {'true': True, 't': True, '1': True,
                 'false': False, 'f': False, '0': False}

        if not isinstance(value, str):
            raise ValueError('invalid literal for boolean. Not a string.')

        lower_value = value.lower()
        #print(lower_value)
        if lower_value in valid:
            return valid[lower_value]
        else:
            raise ValueError('invalid literal for boolean: "%s"' % value)

    def _transBool(self, b):
        #print(type(b))
        if b is True:
            return "True"
        else:
            return "False"


