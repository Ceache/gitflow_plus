__author__ = 'scphantm'

import os
import shutil
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

    REMOTE_ORIGIN = 'remote_origin'

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
        :param repo:
            An instance of the repository object
        """

        #set the configuration system version.  This will be used to
        #determine if the configuration on needs updated or not
        self.version = "0.0.1"

        # set the flow directory name here until I figure out a better way
        self.flowDir = FLOW_DIR

        #make sure we got a copy of the repository object
        if repo is None:
            raise NoRepositoryObject()
        else:
            self.repo = repo

        # the file name for the configuration settings
        self.configFolder = path.join(self.repo.workdir, self.flowDir)
        self.systemConfigFile = path.join(self.configFolder, SYS_CONFIG_FILE)
        self.personalConfigFile = path.join(self.configFolder, PERC_CONFIG_FILE)

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
        ignoreFilename = path.join(self.repo.workdir, '.gitignore')

        f = open(ignoreFilename, 'a+')
        
        for line in f:
            if line == entry:
                return True
                
        f.write(entry)
        f.close

    def _initializeSystemConfig(self):
        """
        This is used to load the system config file into the
        object.  If it doesn't exist, it will create a new one from
        the default methods, save it to the file, and load it
        """
        if path.isfile(self.systemConfigFile):
            print(_('Loading existing system configuration file'))
            self.systemConfig = ConfigObj(self.systemConfigFile, unrepr=False)
        else:
            print(_('Creating new system configuration file'))

            print(self.systemConfigFile)
            print(path.isfile(self.systemConfigFile))
            shutil.copy(self.systemConfigFile, path.isfile(self.systemConfigFile))

            #self.systemConfig = self._buildNewDefaultSystemConfigFile(
            #    ConfigObj(self.systemConfigFile, unrepr=False, create_empty=True))
               
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
                
    def _buildNewDefaultSystemConfigFile(self, config):
        """
        This method is designed to write the basic config settings to a file

        This is
        """

        #config[CONFIG_VERSION] = self.version

        #config[BRANCH_MASTER] = 'master'
        #config[BRANCH_DEVELOP] = 'develop'

        #config[MAINLINE_BRANCHES] = {'master', 'develop'}
        #config[REMOTE_ORIGIN] = 'origin'

        #config['workflows']['version'] = {'VersionCommand'}

        #write the settings to the file
        #config.write()
        return config

    def _buildNewDefaultPersonalConfigFile(self, config):
        """
        This method is designed to write the basic config settings to a file

        This is
        """
        config[REMOTE_ORIGIN] = 'origin'

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