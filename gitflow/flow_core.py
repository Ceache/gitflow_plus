__author__ = 'LID4EC9'

from git import Repo
from flow_exceptions import NotInitialized, GitflowError
from functools import wraps
from flow_documenter import colorText, YELLOW, COLOR_ENABLED
import pprint
import sys


def _procParamString(inputParamDic, key, default):
    ret = default
    if inputParamDic is not None:
        if inputParamDic.get(key) is not None:
            ret = inputParamDic[key]

    return ret


def _procParamBool(inputParamDic, key, default):
    ret = default
    if inputParamDic.get(key) is not None:
        if isinstance(inputParamDic[key], str):
            ret = to_bool(inputParamDic[key])
        else:
            ret = inputParamDic[key]

    return ret


def to_bool(value):
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


def _transBool(b):
    #print(type(b))
    if b is True:
        return "True"
    else:
        return "False"


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


