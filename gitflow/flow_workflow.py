import re
import collections
from gitflow import *
from gitflow.flow_transitions import TransitionFactory
from gitflow.flow_conditions import ConditionFactory
from gitflow.flow_documenter import BLUE, LIGHT_BLUE, GREEN, CYAN, PURPLE, \
    BROWN, LIGHT_GRAY, DARK_GRAY, LIGHT_GREEN, LIGHT_CYAN, \
    LIGHT_RED, LIGHT_PURPLE, YELLOW, WHITE, RED, ENDC, formatValuePair, indentText, \
    colorText, formatWarningKeyValueSet
import pprint


def executeWorkflow(subcmd, args):
    for step in subcmd.steps:
        for condition in step.conditions:
            condition.checkCondition(args)

        step.transition.runTransition(args)


class FlowCommand:
    """
    This is the top level class of the dynamic workflow.  This maps to the
    flow_commands section of the configuration file where it outlines the
    various primary commands in the dynamic workflow.  This also holds which
    workflow is configured for that particular command.
    """
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
    """
    This is the workflow command.  A workflow can be assigned to multiple commands.
    This is how we address duplicate possible workflows.
    """
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
    """
    These subcommands are the individual sub commands within the flow command.  Examples
    would be like start, stop, publish, etc.
    """
    def __init__(self, config, key):
        self.subName = key
        self.usageHelp = config.get(WORK_USAGEHELP)
        self.options = []
        #self.args = []
        self.steps = []

        if config.get(WORK_OPTIONS) is not None:
            options = config.get(WORK_OPTIONS)
            for option in options:
                self.options.append(WorkflowSubcommandOption(option, options.get(option)))

        if config.get(WORK_ARGUMENTS) is not None:
            self.args = config.get(WORK_ARGUMENTS)
            #pprint.pprint(self.args)

        steps = config.get(WORK_STEPS)

        for step in steps:
            for stepkey in step.keys():
                self.steps.append(WorkflowStep(step.get(stepkey), stepkey))
                #print("step: " + stepkey)

    def __str__(self):
        str_list = [colorText(LIGHT_BLUE, indentText(2) + "Sub Command: ", COLOR_ENABLED)
                    + colorText(YELLOW, self.subName, COLOR_ENABLED) + "\n",
                    formatWarningKeyValueSet(indentText(3) + "UsageHelp", self.usageHelp) + "\n"]

        for option in self.options:
            str_list.append(str(option))

        for step in self.steps:
            str_list.append(str(step))

        return ''.join(str_list)


class WorkflowSubcommandOption:
    def __init__(self, option, description):
        self.option = option
        self.description = description

    def __str__(self):
        str_list = ["      Option " + self.option + " - " + self.description + "\n"]
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
                self.conditions.append(ConditionFactory.buildClass(_getMethodName(cond),
                                                                   _getParameters(cond)))

        data = config.get(STEP_TRANSITION)
        self.transition = TransitionFactory.buildClass(
            _getMethodName(data), "transFail", _getParameters(data))

        data = config.get(STEP_COND_CRITICAL_FAIL)
        self.condCriticalFailNext = TransitionFactory.buildClass(
            _getMethodName(data), "transFail", _getParameters(data))

        data = config.get(STEP_COND_NON_CRITICAL_FAIL)
        self.condNonCriticalFailNext = TransitionFactory.buildClass(
            _getMethodName(data), "transFail", _getParameters(data))

        data = config.get(STEP_TRANITION_FAIL)
        self.transFailNext = TransitionFactory.buildClass(
            _getMethodName(data), "transFail", _getParameters(data))

    def __str__(self):
        str_list = [formatValuePair(indentText(3) + "Step", self.stepName) + "\n"]

        if len(self.conditions) == 0:
            str_list.append(colorText(LIGHT_PURPLE, indentText(4) + "No Conditions Set\n", COLOR_ENABLED))
        else:
            for cond in self.conditions:
                str_list.append(str(cond))

        str_list.append(formatWarningKeyValueSet(indentText(4) + "transition",
                                                 self.transition) +"\n")

        str_list.append(formatWarningKeyValueSet(indentText(4) + "condCriticalFailNext",
                                                 self.condCriticalFailNext) + "\n")

        str_list.append(formatWarningKeyValueSet(indentText(4) + "condNonCriticalFailNext",
                                                 self.condNonCriticalFailNext) + "\n")

        str_list.append(formatWarningKeyValueSet(indentText(4) + "transFailNext",
                                                 self.transFailNext) + "\n")

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