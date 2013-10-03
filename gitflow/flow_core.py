__author__ = 'LID4EC9'


BLUE = "\033[0;34m"
LIGHT_BLUE = "\033[1;34m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
PURPLE = "\033[0;35m"
BROWN = "\033[0;33m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_GREEN = "\033[1;32m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_RED = "\033[1;31m"
LIGHT_PURPLE = "\033[1;35m"
YELLOW = "\033[1;33m"
WHITE = "\033[1;37m"
RED = "\033[0;31m"
ENDC = "\033[0;0m"

MODE_COLOR_ENABLED = 1
MODE_COLOR_DIABLED = 0

COLOR_ENABLED = MODE_COLOR_ENABLED

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


def indentText(indentLevel):
    a = 0
    ret = ""
    while a < indentLevel*2:
        a += 1
        ret += " "

    return ret


def colorText(color, text, mode):
    for case in switch(mode):
        if case(MODE_COLOR_ENABLED):
            return color + text + ENDC
        if case(MODE_COLOR_DIABLED):
            return text


def formatValuePair(key, value):
    ret = colorText(LIGHT_BLUE, key, COLOR_ENABLED) + ": "
    ret += colorText(LIGHT_RED, value, COLOR_ENABLED)
    return ret


def formatHeader(text):
    return colorText(LIGHT_PURPLE, text, COLOR_ENABLED)


def formatWarningKeyValueSet(key, value):
    if value is not None:
        titleColor = LIGHT_BLUE
        valueColor = LIGHT_GREEN
        valueText = value
    else:
        titleColor = LIGHT_CYAN
        valueColor = LIGHT_RED
        valueText = "**NOT SET**"

    str_list = [colorText(titleColor, indentText(2) + key, COLOR_ENABLED),
                ": ",
                colorText(valueColor, valueText, COLOR_ENABLED) + "\n"]
    return ''.join(str_list)


class switch(object):
    """
    This class provides the functionality we want. You only need to look at
    this if you want to know how this works. It only needs to be defined
    once, no need to muck around with its internals.
    """
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

# The following example is pretty much the exact use-case of a dictionary,
# but is included for its simplicity. Note that you can include statements
# in each suite.
#v = 'ten'
#for case in switch(v):
#    if case('one'):
#        print 1
#        break
#    if case('two'):
#        print 2
#        break
#    if case('ten'):
#        print 10
#        break
#    if case('eleven'):
#        print 11
#        break
#    if case(): # default, could also just omit condition or 'if True'
#        print "something else!"
#        # No need to break here, it'll stop anyway

# break is used here to look as much like the real thing as possible, but
# elif is generally just as good and more concise.

# Empty suites are considered syntax errors, so intentional fall-throughs
# should contain 'pass'
#c = 'z'
#for case in switch(c):
#    if case('a'): pass # only necessary if the rest of the suite is empty
#    if case('b'): pass
#    # ...
#    if case('y'): pass
#    if case('z'):
#        print "c is lowercase!"
#        break
#    if case('A'): pass
#    # ...
#    if case('Z'):
#        print "c is uppercase!"
#        break
#    if case(): # default
#        print "I dunno what c was!"

# As suggested by Pierre Quentel, you can even expand upon the
# functionality of the classic 'case' statement by matching multiple
# cases in a single shot. This greatly benefits operations such as the
# uppercase/lowercase example above:
#import string
#c = 'A'
#for case in switch(c):
#    if case(*string.lowercase): # note the * for unpacking as arguments
#        print "c is lowercase!"
#        break
#    if case(*string.uppercase):
#        print "c is uppercase!"
#        break
#    if case('!', '?', '.'): # normal argument passing style also applies
#        print "c is a sentence terminator!"
#        break
#    if case(): # default
#        print "I dunno what c was!"

# Since Pierre's suggestion is backward-compatible with the original recipe,
# I have made the necessary modification to allow for the above usage.