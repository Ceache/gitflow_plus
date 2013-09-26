"""
This file contains all the tasks that can be used to assemble workflows

The config file specifies the task chain that is executed for each transition
"""
from gitflow.config.configmanager import ConfigManager
from gitflow.core import GitFlow


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
        #options = inParams.split(',')
        #self.name = options[0]
        #self.workflowName = options[1]
        #self.startBranch = options[2]

        #self.workflow = confMan.getWorkflow(options[1])

    def register_parser(self, parent):
        initMsg = self._getWorkVarFunc()
        p = parent.add_parser(self.flowCommand.flowCommand, help=initMsg)
        p.set_defaults(func=self.run)
        return p

    def run(self, args):
        print('executed ' + self.flowCommand.flowCommand)
        print(str(args))

    def _getWorkVarFunc(self):
        try:
            return self.flowCommand.workflow.description
        except KeyError:
            return ''

class FeatureCommand(GitFlowCommand):
    @classmethod
    def register_parser(cls, parent):
        p = parent.add_parser('feature', help='Manage your feature branches.')
        sub = p.add_subparsers(title='Actions')
        cls.register_list(sub)
        cls.register_start(sub)
        cls.register_finish(sub)
        cls.register_checkout(sub)
        cls.register_diff(sub)
        cls.register_rebase(sub)

        cls.register_publish(sub)
        cls.register_pull(sub)
        cls.register_track(sub)

    #- list
    @classmethod
    def register_list(cls, parent):
        p = parent.add_parser('list',
                              help='List all existing feature branches '
                              'in the local repository.')
        p.set_defaults(func=cls.run_list)
        p.add_argument('-v', '--verbose', action='store_true',
                help='Be verbose (more output).')

    @staticmethod
    def run_list(args):
        gitflow = GitFlow()
        gitflow.start_transaction()
        gitflow.list('feature', 'name', use_tagname=False,
                     verbose=args.verbose)

    #- start
    @classmethod
    def register_start(cls, parent):
        p = parent.add_parser('start', help='Start a new feature branch.')
        p.set_defaults(func=cls.run_start)
        p.add_argument('-F', '--fetch', action='store_true',
                help='Fetch from origin before performing local operation.')
        p.add_argument('name', action=NotEmpty)
        p.add_argument('base', nargs='?')

    @staticmethod
    def run_start(args):
        gitflow = GitFlow()
        # :fixme: Why does the sh-version not require a clean working dir?
        # NB: `args.name` is required since the branch must not yet exist
        # :fixme: get default value for `base`
        gitflow.start_transaction('create feature branch %s (from %s)' % \
                (args.name, args.base))
        try:
            branch = gitflow.create('feature', args.name, args.base,
                                    fetch=args.fetch)
        except (NotInitialized, BaseNotOnBranch):
            # printed in main()
            raise
        except Exception, e:
            die("Could not create feature branch %r" % args.name, e)
        print
        print "Summary of actions:"
        print "- A new branch", branch, "was created, based on", args.base
        print "- You are now on branch", branch
        print ""
        print "Now, start committing on your feature. When done, use:"
        print ""
        print "     git flow feature finish", args.name
        print

    #- finish
    @classmethod
    def register_finish(cls, parent):
        p = parent.add_parser('finish', help='Finish a feature branch.')
        p.set_defaults(func=cls.run_finish)
        p.add_argument('-F', '--fetch', action='store_true',
                help='Fetch from origin before performing local operation.')
        p.add_argument('-r', '--rebase', action='store_true',
                help='Finish branch by rebasing first.')
        p.add_argument('-k', '--keep', action='store_true',
                help='Keep branch after performing finish.')
        p.add_argument('-D', '--force-delete', action='store_true',
                help='Force delete feature branch after finish.')
        p.add_argument('nameprefix', nargs='?')

    @staticmethod
    def run_finish(args):
        gitflow = GitFlow()
        name = gitflow.nameprefix_or_current('feature', args.nameprefix)
        gitflow.start_transaction('finishing feature branch %s' % name)
        gitflow.finish('feature', name,
                       fetch=args.fetch, rebase=args.rebase,
                       keep=args.keep, force_delete=args.force_delete,
                       tagging_info=None)

    #- checkout
    @classmethod
    def register_checkout(cls, parent):
        p = parent.add_parser('checkout',
                help='Check out (switch to) the given feature branch.')
        p.set_defaults(func=cls.run_checkout)
        p.add_argument('nameprefix', action=NotEmpty)

    @staticmethod
    def run_checkout(args):
        gitflow = GitFlow()
        # NB: Does not default to the current branch as `nameprefix` is required
        name = gitflow.nameprefix_or_current('feature', args.nameprefix)
        gitflow.start_transaction('checking out feature branch %s' % name)
        gitflow.checkout('feature', name)

    #- diff
    @classmethod
    def register_diff(cls, parent):
        p = parent.add_parser('diff',
                help='Show a diff of changes since this feature branched off.')
        p.set_defaults(func=cls.run_diff)
        p.add_argument('nameprefix', nargs='?')

    @staticmethod
    def run_diff(args):
        gitflow = GitFlow()
        name = gitflow.nameprefix_or_current('feature', args.nameprefix)
        gitflow.start_transaction('diff for feature branch %s' % name)
        gitflow.diff('feature', name)

    #- rebase
    @classmethod
    def register_rebase(cls, parent):
        p = parent.add_parser('rebase',
                help='Rebase a feature branch on top of develop.')
        p.set_defaults(func=cls.run_rebase)
        p.add_argument('-i', '--interactive', action='store_true',
                help='Start an interactive rebase.')
        p.add_argument('nameprefix', nargs='?')

    @staticmethod
    def run_rebase(args):
        gitflow = GitFlow()
        name = gitflow.nameprefix_or_current('feature', args.nameprefix)
        gitflow.start_transaction('rebasing feature branch %s' % name)
        gitflow.rebase('feature', name, args.interactive)

    #- publish
    @classmethod
    def register_publish(cls, parent):
        p = parent.add_parser('publish',
                help='Publish this feature branch to origin.')
        p.set_defaults(func=cls.run_publish)
        p.add_argument('nameprefix', nargs='?')

    @staticmethod
    def run_publish(args):
        gitflow = GitFlow()
        name = gitflow.nameprefix_or_current('feature', args.nameprefix)
        gitflow.start_transaction('publishing feature branch %s' % name)
        branch = gitflow.publish('feature', name)
        print
        print "Summary of actions:"
        print "- A new remote branch '%s' was created" % branch
        print "- The local branch '%s' was configured to track the remote branch" % branch
        print "- You are now on branch '%s'" % branch
        print

    #- pull
    @classmethod
    def register_pull(cls, parent):
        p = parent.add_parser('pull',
                help='Pull a feature branch from a remote peer.')
        p.set_defaults(func=cls.run_pull)
        p.add_argument('remote', action=NotEmpty,
                       help="Remote repository to pull from.")
        p.add_argument('name', nargs='?',
                help='Name of the feature branch to pull. '
                'Defaults to the current branch, if it is a feature branch.')
        # :todo: implement --prefix
        #p.add-argument('-p', '--prefix',
        #               help='Alternative remote feature branch name prefix.')

    @staticmethod
    def run_pull(args):
        gitflow = GitFlow()
        name = gitflow.name_or_current('feature', args.name, must_exist=False)
        gitflow.start_transaction('pulling remote feature branch %s '
                                  'into local banch %s' % (args.remote, name))
        gitflow.pull('feature', args.remote, name)

    #- track
    @classmethod
    def register_track(cls, parent):
        p = parent.add_parser('track',
                help='Track a feature branch from origin.')
        p.set_defaults(func=cls.run_track)
        p.add_argument('name', action=NotEmpty)

    @staticmethod
    def run_track(args):
        gitflow = GitFlow()
        # NB: `args.name` is required since the branch must not yet exist
        gitflow.start_transaction('tracking remote feature branch %s'
                                  % args.name)
        branch = gitflow.track('feature', args.name)
        print
        print "Summary of actions:"
        print "- A new remote tracking branch '%s' was created" % branch
        print "- You are now on branch '%s'" % branch
        print