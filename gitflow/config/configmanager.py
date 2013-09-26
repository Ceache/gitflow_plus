__author__ = 'scphantm'

import os
import shutil
import gitflow
import re
import json
import pprint
import collections
from os import path
from distutils.version import StrictVersion
from gitflow import i18n
from gitflow.flow_exceptions import NoRepositoryObject

# use ugettext instead of getttext to avoid unicode errors
_ = i18n.language.ugettext


class ConfigManager:
    """
    This is the central configuration manager for the entire system.  This
    class handles everything that the ConfigObj does not do like
    configuring a new system
    """
    # configuration constants
    CONFIG_VERSION = "config_version"
    BRANCH_MASTER = 'branch_master'
    BRANCH_DEVELOP = 'branch_develop'
    MAINLINE_BRANCHES = 'mainline_branches'
    AUTOPUSH_REMOTES = 'autopush_remotes'
    REMOTE_NAME = 'remote_name'

    FLOW_COMMANDS = 'flow_commands'
    SOURCE_BRANCH = "srcBranch"
    SOURCE_WORKFLOW = "workflow"

    WORKFLOWS = 'workflows'
    WORK_OPTIONS = 'options'
    WORK_USAGEHELP = 'usageHelp'
    WORK_STEPS = 'steps'
    STEP_CONDITION = "condition"
    STEP_COND_CRITICAL_FAIL = "condCriticalFailNext"
    STEP_COND_NON_CRITICAL_FAIL = "condNonCriticalFailNext"
    STEP_TRANSITION = "transition"
    STEP_TRANITION_FAIL = "transFailNext"

    WORK_DESCRIPTION = 'description'

    # These are configuration values
    FLOW_DIR = '.flow'

    SYS_CONFIG_FILE = 'gitflowplus.flowini'
    PERC_CONFIG_FILE = 'personal.flowini'

    pdev = re.compile('\$\{branch_develop\}')
    pmast = re.compile('\$\{branch_master\}')
    pcmd = re.compile('\$\{command_name\}')


    # defining a new compare routine to check version numbers.  this is used for the system
    # that upgrades versions from one to the next.
    _compareVersion = lambda self, version1, version2: StrictVersion(version1).__cmp__(version2)

    def __init__(self, repo, initializeBlank=True):
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
            >>> diff()
        """

        #set the configuration system version.  This will be used to
        #determine if the configuration on needs updated or not
        self.version = "0.0.1"

        # set the flow directory name here until I figure out a better way
        self.flowDir = self.FLOW_DIR

        #make sure we got a copy of the repository object
        if repo is None:
            raise NoRepositoryObject()
        else:
            self.repo = repo

        # the file name for the configuration settings
        self.configFolder = path.join(self.repo.working_dir, self.flowDir)
        self.systemConfigFile = path.join(self.configFolder, self.SYS_CONFIG_FILE)
        self.personalConfigFile = path.join(self.configFolder, self.PERC_CONFIG_FILE)

        # Check that the folder exist and load the files
        if not path.isdir(self.configFolder):
            os.mkdir(self.configFolder)

        # these are the system config initializers
        if initializeBlank:
            self._initializeSystemConfig()

        # these are the personal configs
        if initializeBlank:
            self._initializePersonalConfig()

            # This checks the configuration system
            #self._sanityCheck()
        self.checkEntryInGitIgnore(self.personalConfigFile)

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
        f.close

    

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
        config[self.REMOTE_NAME] = 'origin'

        #write the settings to the file
        config.write()
        return config

    def getMainlineBranches(self):
        ret = []
        for item in self.systemConfig[self.MAINLINE_BRANCHES]:
            ret.append(item.strip())
        return ret

    def getAutopushRemotes(self):
        return self.systemConfig[self.AUTOPUSH_REMOTES]

    def getConfigVersion(self):
        return self._getVar(self.CONFIG_VERSION)

    def getBranchMaster(self):
        return self._getVar(self.BRANCH_MASTER)

    def getBranchDevelop(self):
        return self._getVar(self.BRANCH_DEVELOP)

    def getRemoteName(self):
        return self._getVar(self.REMOTE_NAME)

    def _initFlowCommands(self):
        self.flowCommands = []
        for item in self.systemConfig[self.FLOW_COMMANDS]:
            key = item.keys()[0]
            #get the dict under this
            v = item[key]
            self.flowCommands.append(FlowCommand(key, v.get(self.SOURCE_BRANCH),
                                     self.getWorkflow(v.get(self.SOURCE_WORKFLOW))))

    def getFlowCommands(self):
        return self.flowCommands

    def getFlowCommand(self, key):
        for tst in self.flowCommands:
            if key == tst.flowCommand:
                return tst

    def _initWorkflows(self):
        self.workflowCommands = []
        for itm in self.systemConfig[self.WORKFLOWS]:
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
            inputText = self.pcmd.sub(replaceText, inputText)
            return inputText

    def _resolveVariable(self, inputText):
        inputText = self.pdev.sub(self.getBranchDevelop(), inputText)
        inputText = self.pmast.sub(self.getBranchMaster(), inputText)
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
        json_text = open(self.systemConfigFile).read()
        self.systemConfig = json.loads(json_text, object_pairs_hook=collections.OrderedDict)
        #self.printConfig()
        json_text = self._resolveVariable(json_text)
        # print(json_text)
        self.systemConfig = json.loads(json_text, object_pairs_hook=collections.OrderedDict)

        #pprint.pprint(self.systemConfig)

        # Load the workflow commands.  This is done first so they can be mapped
        # to flow commands next
        self._initWorkflows()
        self._initFlowCommands()

        # Now lets do the flow commands, this pulls everything together
        # into congruent commands

        #self.printConfig()

    def printConfig(self):
        print("")
        print(self.CONFIG_VERSION + ": " + self.getConfigVersion())
        print(self.BRANCH_MASTER + ": " + self.getBranchMaster())
        print(self.BRANCH_DEVELOP + ": " + self.getBranchDevelop())

        if self.getAutopushRemotes():
            print(self.AUTOPUSH_REMOTES + ": True")
        else:
            print(self.AUTOPUSH_REMOTES + ": False")

        print(self.REMOTE_NAME + ": " + self.getRemoteName())
        print("")
        print("Mainline Branches:")

        for item in self.getMainlineBranches():
            print("  " + item)

        print("")
        print("Flow Commands:")
        for item in self.getFlowCommands():
            print(str(item))


class FlowCommand:
    def __init__(self, cmdName, branch, workflow):
        self.flowCommand = cmdName
        self.srcBranch = branch
        self.workflow = workflow

    def __str__(self):
        str_list = []
        str_list.append("***" + self.flowCommand + "***" + "\n")
        str_list.append("  srcBranch: " + self.srcBranch + "\n")

        str_list.append(str(self.workflow))

        return ''.join(str_list)


class WorkflowCommand:
    def __init__(self, config, key):
        self.cmdName = key
        self.description = config.get(ConfigManager.WORK_DESCRIPTION)

        self.subCommands = []
        for sub in config:
            if type(config.get(sub)) is collections.OrderedDict:
                self.subCommands.append(WorkflowSubcommand(config.get(sub), sub))

    def __str__(self):
        str_list = []
        str_list.append("  **Workflow: " + self.cmdName + "\n")

        if self.description is not None:
            str_list.append("  **description: " + self.description)

        for sub in self.subCommands:
            str_list.append(str(sub))

        return ''.join(str_list)


class WorkflowSubcommand:
    def __init__(self, config, key):
        self.subName = key
        self.usageHelp = config.get(ConfigManager.WORK_USAGEHELP)
        self.options = []
        self.steps = []

        if config.get(ConfigManager.WORK_OPTIONS) is not None:
            options = config.get(ConfigManager.WORK_OPTIONS)
            for option in options:
                self.options.append(WorkflowSubcommandOption(option, options.get(option)))

        steps = config.get(ConfigManager.WORK_STEPS)

        for step in steps:
            for stepkey in step.keys():
                self.steps.append(WorkflowStep(step.get(stepkey), stepkey))
                #print("step: " + stepkey)

    def __str__(self):
        str_list = []
        str_list.append("  SubCmd: " + self.subName + "\n")

        if self.usageHelp is not None:
            str_list.append("    **UsageHelp: " + self.usageHelp + "\n")

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
        self.condition = config.get(ConfigManager.STEP_CONDITION)
        self.condCriticalFailNext = config.get(ConfigManager.STEP_COND_CRITICAL_FAIL)
        self.condNonCriticalFailNext = config.get(ConfigManager.STEP_COND_NON_CRITICAL_FAIL)
        self.transition = config.get(ConfigManager.STEP_TRANSITION)
        self.transFailNext = config.get(ConfigManager.STEP_TRANITION_FAIL)

    def __str__(self):
        str_list = []
        str_list.append("      Step " + self.stepName + "\n")
        str_list.append("        condition " + str(self.condition) + "\n")
        str_list.append("        condCriticalFailNext " + str(self.condCriticalFailNext) + "\n")
        str_list.append("        condNonCriticalFailNext " + str(self.condNonCriticalFailNext) + "\n")
        str_list.append("        transition " + str(self.transition) + "\n")
        str_list.append("        transFailNext " + str(self.transFailNext) + "\n")
        return ''.join(str_list)


class WorkflowSubcommandOption:
    def __init__(self, option, description):
        self.option = option
        self.description = description

    def __str__(self):
        str_list = []
        str_list.append("      Option " + self.option + " - " + self.description + "\n")
        return ''.join(str_list)


