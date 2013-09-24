__author__ = 'scphantm'

import os
import shutil
import gitflow
import re
import distutils.util
from os import path
from distutils.version import StrictVersion
from gitflow import i18n
from gitflow.flow_exceptions import NoRepositoryObject
from configobj import ConfigObj

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
    WORKFLOWS = 'workflows'

    # These are configuration values
    FLOW_DIR = '.flow'

    SYS_CONFIG_FILE = 'gitflowplus.flowini'
    PERC_CONFIG_FILE = 'personal.flowini'

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

    def _initializeSystemConfig(self):
        """
        This is used to load the system config file into the
        object.  If it doesn't exist, it will copy over the template
        file included in the source distribution and load it.
        """
        if path.isfile(self.systemConfigFile):
            print(_('Loading existing system configuration file'))
            
        else:
            print(_('Creating new system configuration file'))

            templatePath = path.join(os.path.dirname(gitflow.__file__ ), "config/template.gitflowplus.flowini")
            shutil.copy(templatePath, self.systemConfigFile)

        self.systemConfig = ConfigObj(self.systemConfigFile, unrepr=False)
        #self.printConfig()

    def getMainlineBranches(self):
        ret = []
        for item in self.systemConfig[self.MAINLINE_BRANCHES]:
            ret.append(self._resolveVariable(item.strip()))
        return ret

    def getAutopushRemotes(self):
        return distutils.util.strtobool(self.systemConfig[self.AUTOPUSH_REMOTES])

    def getConfigVersion(self):
        return self._getVar(self.CONFIG_VERSION)

    def getBranchMaster(self):
        return self._getVar(self.BRANCH_MASTER)

    def getBranchDevelop(self):
        return self._getVar(self.BRANCH_DEVELOP)

    def getRemoteName(self):
        return self._getVar(self.REMOTE_NAME)

    def getFlowCommands(self):
        ret = []
        for item in self._resolveVariable(self._getVar(self.FLOW_COMMANDS)).split('),('):
            ret.append(self._resolveVariable(item).replace('(', '').replace(')', ''))
        return ret
        #return self._resolveVariable(self._getVar(self.FLOW_COMMANDS)).split('),(')

    def getWorkflows(self):
        return self.systemConfig[self.WORKFLOWS]

    def getWorkflow(self, key):
        return self.systemConfig[self.WORKFLOWS][key]

    def _getVar(self, key):
        return self.systemConfig[key].replace('\n', '').replace('\r', '').replace(' ', '').replace('\'', '')

    def _resolveVariable(self, inputText):
        p = re.compile( '\$\{branch_develop\}')
        inputText = p.sub(self.getBranchDevelop(), inputText)

        p = re.compile( '\$\{branch_master\}')
        inputText = p.sub(self.getBranchMaster(), inputText)
        self.printConfig()
        return inputText
        
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
            print("  " + item)

        print(self.getWorkflows())
        print(self.getWorkflow('gup'))

    def _initializePersonalConfig(self):
        """
        This loads the personal config file into the system.  If it doesn't exist, it 
        will initialize the config file from the defaults and then loads them
        into the object
        """
        if path.isfile(self.personalConfigFile):
            print(_('Loading existing personal configuration file'))
            self.personalConfig = ConfigObj(self.personalConfigFile, unrepr=False)
        else:
            print(_('Creating new personal configuration file'))
            self.personalConfig = self._buildNewDefaultPersonalConfigFile(
                ConfigObj(self.personalConfigFile, unrepr=False, create_empty=True))

    def _buildNewDefaultPersonalConfigFile(self, config):
        """
        This method is designed to write the basic config settings to a file

        This is
        """
        config[self.REMOTE_NAME] = 'origin'

        #write the settings to the file
        config.write()
        return config


"""

    def _init_config(self, master=None, develop=None, prefixes={}, names={},
                     force_defaults=False):
        for setting, default in self.defaults.items():
            if force_defaults:
                value = default
            elif setting == 'gitflow.branch.master':
                value = master
            elif setting == 'gitflow.branch.develop':
                value = develop
            elif setting.startswith('gitflow.prefix.'):
                name = setting[len('gitflow.prefix.'):]
                value = prefixes.get(name, None)
            else:
                name = setting[len('gitflow.'):]
                value = names.get(name, None)
            if value is None:
                value = self.get(setting, default)
            self.set(setting, value)

Here we show creating an empty ConfigObj, setting a filename and some values, and then writing to file :

from configobj import ConfigObj
config = ConfigObj()
config.filename = filename
#
config['keyword1'] = value1
config['keyword2'] = value2
#
config['section1'] = {}
config['section1']['keyword3'] = value3
config['section1']['keyword4'] = value4
#
section2 = {
    'keyword5': value5,
    'keyword6': value6,
    'sub-section': {
        'keyword7': value7
        }
}
config['section2'] = section2
#
config['section3'] = {}
config['section3']['keyword 8'] = [value8, value9, value10]
config['section3']['keyword 9'] = [value11, value12, value13]
#
config.write()
"""