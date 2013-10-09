__author__ = 'LID4EC9'

import inspect
from __init__ import *
from gitflow.flow_transitions import BaseTransition

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


def printConfig(config):
    #indentText(indentLevel)
    print("")
    print(formatHeader("Base Variables:"))
    print(formatValuePair(CONFIG_VERSION, config.getConfigVersion()))
    print(formatValuePair(BRANCH_MASTER, config.getBranchMaster()))
    print(formatValuePair(BRANCH_DEVELOP, config.getBranchDevelop()))

    if config.getAutopushRemotes():
        print(formatValuePair(AUTOPUSH_REMOTES, "True"))
    else:
        print(formatValuePair(AUTOPUSH_REMOTES, "False"))

    print(formatValuePair(REMOTE_NAME, config.getRemoteName()))
    print("")
    print(formatHeader("Mainline Branches:"))

    for item in config.getMainlineBranches():
        print(indentText(1) + colorText(LIGHT_GREEN, item, COLOR_ENABLED))

    print("")
    print(formatHeader("Flow Commands:"))
    for item in config.getFlowCommands():
        print(str(item))


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


def formatWarningKeyValueSet(key, value, mainTitle=LIGHT_BLUE, mainValue=LIGHT_GREEN,
                             warnTitle=LIGHT_CYAN, warnValue=LIGHT_RED):
    if value is not None:
        titleColor = mainTitle
        valueColor = mainValue
        valueText = str(value)
    else:
        titleColor = warnTitle
        valueColor = warnValue
        valueText = "**NOT SET**"

    try:
        if value.TRANS_DEFAULT:
            titleColor = warnTitle
            valueColor = warnValue
            valueText = "**NOT SET: Using default " + value.__class__.__name__ + "**"
    except (AttributeError, TypeError):
        pass

    str_list = [colorText(titleColor, key, COLOR_ENABLED),
                ": ",
                colorText(valueColor, valueText, COLOR_ENABLED)]
    return ''.join(str_list)