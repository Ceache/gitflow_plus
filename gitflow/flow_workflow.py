import re
import collections
from gitflow import *
from gitflow.flow_transitions import TransitionFactory
from gitflow.flow_conditions import ConditionFactory
#from gitflow.flow_config import ConfigManager


class FlowCommand:
    def __init__(self, cmdName, branch, workflow):
        self.flowCommand = cmdName
        self.srcBranch = branch
        self.workflow = workflow

    def __str__(self):
        str_list = [colorText(YELLOW, self.flowCommand, COLOR_ENABLED) + "\n",
                    formatValuePair(indentText(1) + "srcBranch", self.srcBranch) + "\n",
                    str(self.workflow)]

        return ''.join(str_list)


class WorkflowCommand:
    def __init__(self, config, key):
        self.cmdName = key
        self.description = config.get(WORK_DESCRIPTION)

        self.subCommands = []
        for sub in config:
            if type(config.get(sub)) is collections.OrderedDict:
                self.subCommands.append(WorkflowSubcommand(config.get(sub), sub))

    def __str__(self):
        str_list = [formatValuePair(indentText(1) + "Workflow", self.cmdName) + "\n"]

        if self.description is not None:
            str_list.append(formatValuePair(indentText(1) + "description", self.description) + "\n")

        for sub in self.subCommands:
            str_list.append(str(sub))

        return ''.join(str_list)


class WorkflowSubcommand:
    def __init__(self, config, key):
        self.subName = key
        self.usageHelp = config.get(WORK_USAGEHELP)
        self.options = []
        self.args = []
        self.steps = []

        if config.get(WORK_OPTIONS) is not None:
            options = config.get(WORK_OPTIONS)
            for option in options:
                self.options.append(WorkflowSubcommandOption(option, options.get(option)))

        if config.get(WORK_ARGUMENTS) is not None:
            args = config.get(WORK_ARGUMENTS)
            for arg in args:
                self.args.append(WorkflowSubcommandArguments(arg, args.get(arg)))

        steps = config.get(WORK_STEPS)

        for step in steps:
            for stepkey in step.keys():
                self.steps.append(WorkflowStep(step.get(stepkey), stepkey))
                #print("step: " + stepkey)

    def __str__(self):
        str_list = [colorText(LIGHT_BLUE, indentText(2) + "Sub Command: ", COLOR_ENABLED)
                    + colorText(YELLOW, self.subName, COLOR_ENABLED) + "\n",
                    formatWarningKeyValueSet("UsageHelp", self.usageHelp)]

        for option in self.options:
            str_list.append(str(option))

        for step in self.steps:
            str_list.append(str(step))

        return ''.join(str_list)


class WorkflowStep:
    def __init__(self, config, key):
        #pprint.pprint(config)
        #print(key)
        self.stepName = key
        conditionsList = config.get(STEP_CONDITIONS)

        self.conditions = []

        if conditionsList is not None:
            for cond in conditionsList:
                self.conditions.append(ConditionFactory.buildClass(self._getMethodName(cond),
                                                                   self._getParameters(cond)))

        data = config.get(STEP_TRANSITION)
        self.transition = TransitionFactory.buildClass(
            self._getMethodName(data), "transFail", self._getParameters(data))

        data = config.get(STEP_COND_CRITICAL_FAIL)
        self.condCriticalFailNext = TransitionFactory.buildClass(
            self._getMethodName(data), "transFail", self._getParameters(data))

        data = config.get(STEP_COND_NON_CRITICAL_FAIL)
        self.condNonCriticalFailNext = TransitionFactory.buildClass(
            self._getMethodName(data), "transFail", self._getParameters(data))

        data = config.get(STEP_TRANITION_FAIL)
        self.transFailNext = TransitionFactory.buildClass(
            self._getMethodName(data), "transFail", self._getParameters(data))

    def __str__(self):
        str_list = ["      Step " + self.stepName + "\n",
                    "        transition \n" + str(self.transition) + "\n",
                    "        condCriticalFailNext \n" + str(self.condCriticalFailNext) + "\n",
                    "        condNonCriticalFailNext \n" + str(self.condNonCriticalFailNext) + "\n",
                    "        transFailNext \n" + str(self.transFailNext) + "\n"]

        for cond in self.conditions:
            str_list.append(str(cond))

        return ''.join(str_list)


class WorkflowSubcommandArguments:
    def __init__(self, arg, description):
        self.arg = arg
        self.description = description

    def __str__(self):
        str_list = ["      arg " + self.arg + " - " + self.description + "\n"]
        return ''.join(str_list)


class WorkflowSubcommandOption:
    def __init__(self, option, description):
        self.option = option
        self.description = description

    def __str__(self):
        str_list = ["      Option " + self.option + " - " + self.description + "\n"]
        return ''.join(str_list)


def _getParameters(lookin):
    if lookin is None:
        return None
    else:
        p = re.compile("(?<=\()(.*?)(?=\))")
        d = collections.OrderedDict()

        for m in p.finditer(lookin):
            conds = m.group().split(",")
            for cond in conds:
                ltemp = cond.split("=")
                if len(ltemp) == 2:
                    d[str(ltemp[0].strip().rstrip())] = str(ltemp[1].strip().rstrip())
                    #pprint.pprint(d)
        return d


def _getMethodName(lookin):
    if lookin is not None:
        return re.sub("\(([^\)]+)\)|\(\)", "", lookin)
    else:
        return None