__author__ = 'scphantm'
from distutils.version import StrictVersion


class ConfigManager:
    """
    This is the central configuration manager for the entire system.  This
    class handles everything that the ConfigObj does not do like
    configuring a new system
    """

    # defining a new compare routine to check version numbers.  this is used for the system
    # that upgrades versions from one to the next.
    _compareVersion = lambda self, version1, version2: StrictVersion(version1).__cmp__(version2)

    def __init__(self):
        """
        This is the constructor.  Here we set the initial fields for the
        configuration system
        """
        self.version = "0.0.1"

        # set the flow directory name here until I figure out a better way
        self.flowDir = ".flow"

    def initializeNewConfig(self):
        """
        This method will configure a new blank system and load it with
        the default settings

        """
        pass

    def loadConfig(self):
        pass
