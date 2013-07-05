__author__ = 'scphantm'

import os
from os import path
from distutils.version import StrictVersion
from pygit2 import Repository
from exceptions import NoRepositoryObject
from configobj import ConfigObj


class ConfigManager:
    """
    This is the central configuration manager for the entire system.  This
    class handles everything that the ConfigObj does not do like
    configuring a new system
    """

    # defining a new compare routine to check version numbers.  this is used for the system
    # that upgrades versions from one to the next.
    _compareVersion = lambda self, version1, version2: StrictVersion(version1).__cmp__(version2)

    def __init__(self, repo):
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
        self.flowDir = ".flow"

        # the file name for the configuration settings
        self.configFile = "gitflowplus.ini"

        #make sure we got a copy of the repository object
        if repo is None:
            raise NoRepositoryObject()
        else:
            self.repo = repo

    def initializeNewConfig(self):
        """
        This method will configure a new blank system and load it with
        the default settings

        """
        filename = path.join(self.repo.working_dir, self.flowDir, self.configFile)

        # create the config folder if it doesn't exist
        if not self._isFolderExist(self):
            os.mkdir(path.join(self.repo.working_dir, self.flowDir))

        # create the blank file
        self.config = ConfigObj(filename, unrepr=False, create_empty=True)

    def loadConfig(self):
        """
        This takes all the information given during the initialization of the
        object and loads the configuration system so it can be used elseware in
        the system.
        :return:
        """

        pass

    def _isFolderExist(self):
        """
        This checks the repository and determines if the configuration folder
        exists
        :return boolean:
        """
        return path.isdir(path.join(self.repo.working_dir, self.flowDir))

    def _isConfigFileExist(self):
        """
        This checks to see if the configuation file exists and can be properly
        parsed
        :return boolean:
        """
        return path.isfile(path.join(self.repo.working_dir, self.flowDir, self.configFile))