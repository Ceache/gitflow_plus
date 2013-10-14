__author__ = 'scphantm'

# https://bitbucket.org/BruceEckel/python-3-patterns-idioms/src/b1be62c8c0e547f271704adbbbfcb2f6d1caf5a0/code/StateMachine/vendingmachine/VendingMachine.py?at=default
# https://python-3-patterns-idioms-test.readthedocs.org/en/latest/StateMachine.html
# http://stackoverflow.com/questions/226976/how-can-i-know-in-git-if-a-branch-has-been-already-merged-into-master


import os
import shutil
import gitflow
import json
import collections
import gitdb
from git.repo import Repo

from os import path
from distutils.version import StrictVersion
from __init__ import *
from gitflow import i18n
from gitflow.flow_exceptions import NoRepositoryObject

import re
from gitflow.flow_transitions import TransitionFactory
from gitflow.flow_documenter import BLUE, LIGHT_BLUE, GREEN, CYAN, PURPLE, \
    BROWN, LIGHT_GRAY, DARK_GRAY, LIGHT_GREEN, LIGHT_CYAN, \
    LIGHT_RED, LIGHT_PURPLE, YELLOW, WHITE, RED, ENDC, formatValuePair, indentText, \
    colorText, formatWarningKeyValueSet
import pprint

from flow_core import requires_repo, getParamBool, boolToString
import pprint


from gitflow.flow_core import *

# use ugettext instead of getttext to avoid unicode errors
_ = i18n.language.ugettext
get_class = lambda x: globals()[x]


class ConfigManager(object):
    """
    This is the central configuration manager for the entire system.  This
    class handles everything that the ConfigObj does not do like
    configuring a new system
    """
    _shared_state = {}

    # defining a new compare routine to check version numbers.  this is used for the system
    # that upgrades versions from one to the next.
    _compareVersion = lambda self, version1, version2: StrictVersion(version1).__cmp__(version2)

    def __init__(self):
        """
        This is the constructor.  Here we set the initial fields for the
        configuration system

        Parameters:

        repo : GitFlow
            An instance of the repository object

        initializeBlank : boolean
            Indicates to create a new repo of one doesnt exists.  Defaults to True.

        Examples::

            # Changes in the working tree not yet staged for the next commit
            diff()
        """
        self.__dict__ = self._shared_state

    def loadConfig(self, initializeBlank=True, repo_dir=".", existingRepo=None):
        self.repo = None

        # repository has a property called workingdir.
        # this block is saying if what you passed is a repo object
        # then set the working_dir field to the path in the object
        # otherwise we are assuming you sent a directory path
        #if isinstance(working_dir, Repo):
        #    self.working_dir = working_dir.working_dir
        #else:

        #self.working_dir = working_dir

        # todo : not sure if this is still needed, if not get rid of it
        #self.git = Git(self.working_dir)

        # try to initialize the repo object.  if it fails, keep going
        # the field will just be null and other error checks take care
        # of making sure the repo exists before trying to put anything
        # in it.
        try:
            if existingRepo is None:
                self.repo = Repo(repo_dir)
            else:
                self.repo = existingRepo

            if self.repo is None:
                raise NoRepositoryObject()
        except GitflowError:
            pass

        self.version = "0.0.1"
        self.flowDir = FLOW_DIR

        self.configFolder = path.join(self.repo.working_dir, self.flowDir)
        self.systemConfigFile = path.join(self.configFolder, SYS_CONFIG_FILE)
        self.personalConfigFile = path.join(self.configFolder, PERC_CONFIG_FILE)
        if not path.isdir(self.configFolder):
            os.mkdir(self.configFolder)

        if initializeBlank:
            self._initializeSystemConfig()

        #if initializeBlank:
        #    self._initializePersonalConfig()

            # This checks the configuration system
            #self._sanityCheck()
        self.checkEntryInGitIgnore(PERC_CONFIG_FILE)

    def checkEntryInGitIgnore(self, entry):
        """
        This checks the git ignore file for the entry you specify.  If it doesn't exists
        it adds it, if it does exist, it ignores it and leaves everything untouched
        :param entry:
            The entry you want added to the ignore file.
        """
        ignoreFilename = path.join(self.repo.working_dir, '.gitignore')

        f = open(ignoreFilename, 'a+')

        for line in f:
            if line == entry:
                return True

        f.write(entry)
        f.close()


    def _initializePersonalConfig(self):
        """
        This loads the personal config file into the system.  If it doesn't exist, it
        will initialize the config file from the defaults and then loads them
        into the object
        """
        if path.isfile(self.personalConfigFile):
            print(_('Loading existing personal configuration file'))
            self.personalConfig = json.loads(open(self.personalConfigFile).read())
        else:
            print(_('Creating new personal configuration file'))

    def _buildNewDefaultPersonalConfigFile(self, config):
        """
        This method is designed to write the basic config settings to a file

        This is
        """
        config[REMOTE_NAME] = 'origin'

        #write the settings to the file
        config.write()
        return config

    def getMainlineBranches(self):
        ret = []
        for item in self.systemConfig[MAINLINE_BRANCHES]:
            ret.append(item.strip())
        return ret

    def getAutopushRemotes(self):
        return self.systemConfig[AUTOPUSH_REMOTES]

    def getConfigVersion(self):
        return self._getVar(CONFIG_VERSION)

    def getBranchMaster(self):
        return self._getVar(BRANCH_MASTER)

    def getBranchDevelop(self):
        return self._getVar(BRANCH_DEVELOP)

    def getRemoteName(self):
        return self._getVar(REMOTE_NAME)

    def _initFlowCommands(self):
        self.flowCommands = []
        for item in self.systemConfig[FLOW_COMMANDS]:
            key = item.keys()[0]
            #get the dict under this
            v = item[key]
            self.flowCommands.append(FlowCommand(key, v.get(SOURCE_BRANCH),
                                                 self.getWorkflow(v.get(SOURCE_WORKFLOW))))

    def getFlowCommands(self):
        return self.flowCommands

    def getFlowCommand(self, key):
        for tst in self.flowCommands:
            if key == tst.flowCommand:
                return tst

    def _initWorkflows(self):
        self.workflowCommands = []
        for itm in self.systemConfig[WORKFLOWS]:
            key = itm.keys()[0]
            # print(key)
            # pprint.pprint(itm[key])
            self.workflowCommands.append(WorkflowCommand(itm[key], key))

    def getWorkflows(self):
        return self.workflowCommands

    def getWorkflow(self, key):
        for cmd in self.workflowCommands:
            if key == cmd.cmdName:
                return cmd
        return None

    def _getVar(self, key):
        return self.systemConfig[key].replace('\n', '').replace('\r', '').replace(' ', '').replace('\'', '')

    def resolveConfig(self, inputText, replaceText):
        if ((inputText is not None) and (replaceText is not None)):
            inputText = pcmd.sub(replaceText, inputText)
            return inputText

    def resolveVariable(self, inputText):
        if inputText is not None:
            inputText = pdev.sub(self.getBranchDevelop(), inputText)
            inputText = pmast.sub(self.getBranchMaster(), inputText)

        return inputText

    def _initializeSystemConfig(self):
        """
        This is used to load the system config file into the
        object.  If it doesn't exist, it will copy over the template
        file included in the source distribution and load it.
        """
        if path.isfile(self.systemConfigFile):
            #print(_('Loading existing system configuration file'))
            pass
        else:
            #print(_('Creating new system configuration file'))
            templatePath = path.join(os.path.dirname(gitflow.__file__), "config/template.gitflowplus.flowini")
            shutil.copy(templatePath, self.systemConfigFile)

        # Order is VERY important in this workflow, so we are parsing the json
        # file into an ordereddict to mantain its order

        #We are parsing the file twice because we need to resolve variables.  In order
        # to get the info to resolve those variables, we need to parse it once first
        f = open(self.systemConfigFile)
        json_text = f.read()
        f.close()

        self.systemConfig = json.loads(json_text, object_pairs_hook=collections.OrderedDict)
        #self.printConfig()
        json_text = self.resolveVariable(json_text)
        # print(json_text)
        self.systemConfig = json.loads(json_text, object_pairs_hook=collections.OrderedDict)

        # Load the workflow commands.  This is done first so they can be mapped
        # to flow commands next
        self._initWorkflows()
        self._initFlowCommands()



def executeWorkflow(subcmd, args):
    for step in subcmd.steps:
        for condition in step.conditions:
            if condition.checkCondition(args):
                print(colorText(LIGHT_GREEN, "condition passed", COLOR_ENABLED))
            else:
                print(colorText(LIGHT_RED, "raise condition error", COLOR_ENABLED))

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


class BaseCondition():
    PASS = 1
    CRITICAL_FAIL = 2
    WARNING = 3

    PARAM_VALID = 'valid'
    PARAM_CRITICAL = 'critical'

    def __init__(self, params):
        # for conditions, the parameters are optional.  If
        # an option is not entered, its defaulted to TRUE
        self.valid = getParamBool(params, self.PARAM_VALID, True)
        self.critical = getParamBool(params, self.PARAM_CRITICAL, True)
        self.config = ConfigManager()
        self.rawParams = params

    def checkCondition(self, args):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        str_list = [formatValuePair(indentText(4) + "Condition", self.__class__.__name__) + "\n",
                    formatValuePair(indentText(5) + "valid Check", boolToString(self.valid)) + "\n",
                    formatValuePair(indentText(5) + "critical Check", boolToString(self.critical)) + "\n"]

        return ''.join(str_list)

    def _checkCondition(self, testValue, warnMsg):
        if self.valid == testValue:
            # we got the answer we wanted.  send a true
            return True
        else:
            if self.critical:
                # this is a critical failure, send a false
                return False
            else:
                # It is a non critical failure.  Log the warning
                # and return a true
                warn(warnMsg)
                return True


def _flipBool(inBool):
    """
    A simple method that flips the boolean.  This is needed
    to keep the configuration file straight
    """
    if inBool:
        return False
    else:
        return True


class condIsClean(BaseCondition):
    @requires_repo
    def checkCondition(self, args):
        """
        Returns whether or not the current working directory contains
        uncommitted changes.
        """

        # for the check to work, the response from is_dirty
        # must be reversed
        return self._checkCondition(_flipBool(self.config.repo.is_dirty(untracked_files=True)),
                                    _('WARN: Non-Critical condition IsClean failed'))


class condBranchExist(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + boolToString(self.valid))
        print("  critical Check: " + boolToString(self.critical))
        print("  class Name: " + self.__class__.__name__)


class condPushRemote(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + boolToString(self.valid))
        print("  critical Check: " + boolToString(self.critical))
        print("  class Name: " + self.__class__.__name__)


class condIsNextMaster(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + boolToString(self.valid))
        print("  critical Check: " + boolToString(self.critical))
        print("  class Name: " + self.__class__.__name__)


class condDefault(BaseCondition):
    def checkCondition(self, args):
        print("  valid Check: " + boolToString(self.valid))
        print("  critical Check: " + boolToString(self.critical))
        print("  class Name: " + self.__class__.__name__)


class ConditionFactory():
    @staticmethod
    def buildClass(condition, params):
        constructor = globals()[condition]
        instance = constructor(params)
        return instance
