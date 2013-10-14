__author__ = 'LID4EC9'

from functools import wraps
import sys

from flow_exceptions import NotInitialized
from flow_documenter import colorText, YELLOW, COLOR_ENABLED


def getParamString(inputParamDic, key, default=None):
    """
    Gets a value from a dictionary as a string.  the real purpose
    of this is to add a default value parameter to your values.
    :param inputParamDic:
    :param key:
    :param default:
    """
    ret = default
    if inputParamDic is not None:
        if inputParamDic.get(key) is not None:
            ret = inputParamDic[key]

    return ret


def getParamBool(inputParamDic, key, default=None):
    """
    Gets the key specified from the specified dictionary object and returns
    the result as a boolean.  This uses the method :method:`stringToBool` to convert the
    value.
    :param inputParamDic:
    :param key:
    :param default:
    """
    ret = default
    if inputParamDic.get(key) is not None:
        if isinstance(inputParamDic[key], str):
            ret = stringToBool(inputParamDic[key])
        else:
            ret = inputParamDic[key]

    return ret


def boolToString(b):
    """
    This converts a boolean value to a string.
    :param b:
    """

    if b is None:
        raise ValueError('invalid literal for boolean: None')

    if b is True:
        return "True"
    else:
        return "False"


def stringToBool(value):
    """
    This converts a string to a boolean
    :param value:
    """
    valid = {'true': True, 't': True, '1': True, 'yes': True,
             'false': False, 'f': False, '0': False, 'no': False}

    if not isinstance(value, str):
        raise ValueError('invalid literal for boolean. Not a string.')

    lower_value = value.lower()
    #print(lower_value)
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('invalid literal for boolean: "%s"' % value)


def info(*texts):
    """
    Takes in an array of strings and prints them, one item of the array on each line
    :param texts:
    """
    for txt in texts:
        print(txt)


def warn(*texts):
    """
    Takes in an array of text strings and prints them to the stderr stream
    :param texts:
    """
    for txt in texts:
        sys.stderr.write(colorText(YELLOW, txt + "\n", COLOR_ENABLED))


def requires_repo(f):
    """
    This is an annotation method that is used to check that
    a git repository is initialized.  if it doesn't, an exception is raised
    :param f:
    :return boolean:
    :raise NotInitialized:
    """

    @wraps(f)
    def _inner(self, *args, **kwargs):
        if self.config.repo is None:
            raise NotInitialized()
        return f(self, *args, **kwargs)

    return _inner


