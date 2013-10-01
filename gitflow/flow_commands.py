"""
This file contains all the tasks that can be used to assemble workflows

The config file specifies the task chain that is executed for each transition
"""
import argparse
from gitflow.config.configmanager import ConfigManager
from gitflow.core import GitFlow
from pprint import pprint

class GitFlowCommand(object):
    """
    This is just an empty class to serve as the base class for all command line
    level sub commands.  Since the git-flow loader will auto-detect all
    subclasses, implementing a new subcommand is as easy as subclassing the
    :class:`GitFlowCommand`.
    """

    @classmethod
    def register_parser(cls, parent):
        """
        This inserts the parameters into the arg parser.  If you are creating
        a subcommand and want the command to show up when you do git flow help,
        enter the code to add it to the parent argument parser here
        :param parent:
            The parent argument parser
        """
        raise NotImplementedError("Implement this method in a subclass.")

    @staticmethod
    def run(args):
        """
        This is the actual logic of the command you are creating.  Everything
        the command does goes here
        :param args:
            The arguments passed from the command line to here
        """
        raise NotImplementedError("Implement this method in a subclass.")


class GitFlowSimpleTask(object):
    """
    This class identifies very simple tasks in the workflow.  These would
    be akin to one line commands like git add -A and the like
    """

    @staticmethod
    def run(args):
        """
        This is the actual logic of the command you are creating.  Everything
        the command does goes here
        :param args:
            The arguments passed from the command line to here
        """
        raise NotImplementedError("Implement this method in a subclass.")


class VersionCommand(GitFlowCommand):
    """
    This command outside of the workflow system will simply print the version of gitflow plus
    """
    @classmethod
    def register_parser(cls, parent):
        """
        see GitFlowCommand.register_parser comments
        :param cls:
        :param parent:
        :return:
        """
        p = parent.add_parser('version', help='Show the version of gitflow.')
        p.set_defaults(func=cls.run)
        return p

    @staticmethod
    def run(args):
        """
        see GitFlowCommand.run comments
        :param args:
        :return:
        """
        from gitflow import __version__

        print(__version__)


class InitCommand(GitFlowCommand):
    """
    This is a hard command outside of the workflow.  This initializes the repository
    so it can be used with gitflow.
    """
    @classmethod
    def register_parser(cls, parent):
        """
        see GitFlowCommand.register_parser comments
        :param cls:
        :param parent:
        :return:
        """
        initMsg = "Initialize a repository for gitflow."
        p = parent.add_parser('init', help=initMsg)
        # p.add_argument('-f', '--force', action='store_true',
        #                help='Force reinitialization of the gitflow preferences.')
        # p.add_argument('-d', '--defaults', action='store_true',
        #                dest='use_defaults',
        #                help='Use default branch naming conventions and prefixes.')
        p.set_defaults(func=cls.run)
        return p

    @staticmethod
    def run(args):
        """
        see GitFlowCommand.run comments
        :param args:
        :return:
        """
        
        print('executed InitCommand')


class DynamicCommand():

    def __init__(self, cmd):
        self.flowCommand = cmd
        #           self.subName = key
        #           self.usageHelp = config.get(ConfigManager.WORK_USAGEHELP)
        #           self.options = []
        #           self.steps = []

    
    @staticmethod
    def run(args):
        #c = ConfigManager(GitFlow())

        #print('executed ' + self.flowCommand.flowCommand)
        pprint(str(args))

class NotEmpty(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            raise argparse.ArgumentError(self, 'must not by empty.')
        setattr(namespace, self.dest, values)
