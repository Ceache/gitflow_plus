class StatusCommand(GitFlowCommand):
    @classmethod
    def register_parser(cls, parent):
        p = parent.add_parser('status', help='Show some status.')
        p.set_defaults(func=cls.run)

    @staticmethod
    def run(args):
        gitflow = GitFlow()
        for name, hexsha, is_active_branch in gitflow.status():
            if is_active_branch:
                prefix = '*'
            else:
                prefix = ' '
            info('%s %s: %s' % (prefix, name, hexsha[:7]))


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


class ReleaseCommand(GitFlowCommand):
    @classmethod
    def register_parser(cls, parent):
        p = parent.add_parser('release', help='Manage your release branches.')
        p.add_argument('-v', '--verbose', action='store_true',
           help='Be verbose (more output).')
        sub = p.add_subparsers(title='Actions')
        cls.register_list(sub)
        cls.register_start(sub)
        cls.register_finish(sub)
        cls.register_publish(sub)
        cls.register_track(sub)

    #- list
    @classmethod
    def register_list(cls, parent):
        p = parent.add_parser('list',
                              help='Lists all existing release branches '
                              'in the local repository.')
        p.set_defaults(func=cls.run_list)
        p.add_argument('-v', '--verbose', action='store_true',
                help='Be verbose (more output).')

    @staticmethod
    def run_list(args):
        gitflow = GitFlow()
        gitflow.start_transaction()
        gitflow.list('release', 'version', use_tagname=True,
                     verbose=args.verbose)

    #- start
    @classmethod
    def register_start(cls, parent):
        p = parent.add_parser('start', help='Start a new release branch.')
        p.set_defaults(func=cls.run_start)
        p.add_argument('-F', '--fetch', action='store_true',
                       #:todo: get "origin" from config
                help='Fetch from origin before performing local operation.')
        p.add_argument('version', action=NotEmpty)
        p.add_argument('base', nargs='?')

    @staticmethod
    def run_start(args):
        gitflow = GitFlow()
        # NB: `args.version` is required since the branch must not yet exist
        # :fixme: get default value for `base`
        gitflow.start_transaction('create release branch %s (from %s)' % \
                (args.version, args.base))
        try:
            branch = gitflow.create('release', args.version, args.base,
                                    fetch=args.fetch)
        except (NotInitialized, BranchTypeExistsError, BaseNotOnBranch):
            # printed in main()
            raise
        except Exception, e:
            die("Could not create release branch %r" % args.version, e)
        print "Follow-up actions:"
        print "- Bump the version number now!"
        print "- Start committing last-minute fixes in preparing your release"
        print "- When done, run:"
        print
        print "     git flow release finish", args.version

    #- finish
    @classmethod
    def register_finish(cls, parent):
        p = parent.add_parser('finish', help='Finish a release branch.')
        p.set_defaults(func=cls.run_finish)
        p.add_argument('-F', '--fetch', action='store_true',
                help='Fetch from origin before performing local operation.')
        p.add_argument('-p', '--push', action='store_true',
                       #:todo: get "origin" from config
                       help="Push to origin after performing finish.")
        p.add_argument('-k', '--keep', action='store_true',
                help='Keep branch after performing finish.')
        p.add_argument('version', nargs='?')

        g = p.add_argument_group('tagging options')
        g.add_argument('-n', '--notag', action='store_true',
                       help="Don't tag this release.")
        g.add_argument('-m', '--message',
                       help="Use the given tag message.")
        g.add_argument('-s', '--sign', action='store_true',
                help="Sign the release tag cryptographically.")
        g.add_argument('-u', '--signingkey',
                help="Use the given GPG-key for the digital signature "
                     "instead of the default git uses (implies -s).")

    @staticmethod
    def run_finish(args):
        gitflow = GitFlow()
        version = gitflow.name_or_current('release', args.version)
        gitflow.start_transaction('finishing release branch %s' % version)
        tagging_info = None
        if not args.notag:
            tagging_info = dict(
                sign=args.sign or args.signingkey,
                signingkey=args.signingkey,
                message=args.message)
        release = gitflow.finish('release', version,
                                 fetch=args.fetch, rebase=False,
                                 keep=args.keep, force_delete=False,
                                 tagging_info=tagging_info)

    #- publish
    @classmethod
    def register_publish(cls, parent):
        p = parent.add_parser('publish',
                help='Publish this release branch to origin.')
        p.set_defaults(func=cls.run_publish)
        p.add_argument('version', nargs='?')

    @staticmethod
    def run_publish(args):
        gitflow = GitFlow()
        version = gitflow.name_or_current('release', args.version)
        gitflow.start_transaction('publishing release branch %s' % version)
        branch = gitflow.publish('release', version)
        print
        print "Summary of actions:"
        print "- A new remote branch '%s' was created" % branch
        print "- The local branch '%s' was configured to track the remote branch" % branch
        print "- You are now on branch '%s'" % branch
        print

    #- track
    @classmethod
    def register_track(cls, parent):
        p = parent.add_parser('track',
                help='Track a release branch from origin.')
        p.set_defaults(func=cls.run_track)
        p.add_argument('version', action=NotEmpty)

    @staticmethod
    def run_track(args):
        gitflow = GitFlow()
        # NB: `args.version` is required since the branch must not yet exist
        gitflow.start_transaction('tracking remote release branch %s'
                                  % args.version)
        branch = gitflow.track('release', args.version)
        print
        print "Summary of actions:"
        print "- A new remote tracking branch '%s' was created" % branch
        print "- You are now on branch '%s'" % branch
        print


class HotfixCommand(GitFlowCommand):
    @classmethod
    def register_parser(cls, parent):
        p = parent.add_parser('hotfix', help='Manage your hotfix branches.')
        p.add_argument('-v', '--verbose', action='store_true',
           help='Be verbose (more output).')
        sub = p.add_subparsers(title='Actions')
        cls.register_list(sub)
        cls.register_start(sub)
        cls.register_finish(sub)
        cls.register_publish(sub)

    #- list
    @classmethod
    def register_list(cls, parent):
        p = parent.add_parser('list',
                              help='Lists all existing hotfix branches '
                              'in the local repository.')
        p.set_defaults(func=cls.run_list)
        p.add_argument('-v', '--verbose', action='store_true',
                help='Be verbose (more output).')

    @staticmethod
    def run_list(args):
        gitflow = GitFlow()
        gitflow.start_transaction()
        gitflow.list('hotfix', 'version', use_tagname=True,
                     verbose=args.verbose)

    #- start
    @classmethod
    def register_start(cls, parent):
        p = parent.add_parser('start', help='Start a new hotfix branch.')
        p.set_defaults(func=cls.run_start)
        p.add_argument('-F', '--fetch', action='store_true',
                       #:todo: get "origin" from config
                help='Fetch from origin before performing local operation.')
        p.add_argument('version', action=NotEmpty)
        p.add_argument('base', nargs='?')

    @staticmethod
    def run_start(args):
        gitflow = GitFlow()
        # NB: `args.version` is required since the branch must not yet exist
        # :fixme: get default value for `base`
        gitflow.start_transaction('create hotfix branch %s (from %s)' % \
                (args.version, args.base))
        try:
            branch = gitflow.create('hotfix', args.version, args.base,
                                    fetch=args.fetch)
        except (NotInitialized, BranchTypeExistsError, BaseNotOnBranch):
            # printed in main()
            raise
        except Exception, e:
            die("Could not create hotfix branch %r" % args.version, e)
        print
        print "Summary of actions:"
        print "- A new branch", branch, "was created, based on", args.base
        print "- You are now on branch", branch
        print ""
        print "Follow-up actions:"
        print "- Bump the version number now!"
        print "- Start committing your hot fixes"
        print "- When done, run:"
        print
        print "     git flow hotfix finish", args.version

    #- finish
    @classmethod
    def register_finish(cls, parent):
        p = parent.add_parser('finish', help='Finish a hotfix branch.')
        p.set_defaults(func=cls.run_finish)
        p.add_argument('-F', '--fetch', action='store_true',
                help='Fetch from origin before performing local operation.')
        p.add_argument('-p', '--push', action='store_true',
                       #:todo: get "origin" from config
                       help="Push to origin after performing finish.")
        p.add_argument('-k', '--keep', action='store_true',
                help='Keep branch after performing finish.')
        p.add_argument('version', nargs='?')

        g = p.add_argument_group('tagging options')
        g.add_argument('-n', '--notag', action='store_true',
                       help="Don't tag this hotfix.")
        g.add_argument('-m', '--message',
                       help="Use the given tag message.")
        g.add_argument('-s', '--sign', action='store_true',
                help="Sign the hotfix tag cryptographically.")
        g.add_argument('-u', '--signingkey',
                help="Use this given GPG-key for the digital signature "
                     "instead of the default git uses (implies -s).")

    @staticmethod
    def run_finish(args):
        gitflow = GitFlow()
        version = gitflow.name_or_current('hotfix', args.version)
        gitflow.start_transaction('finishing hotfix branch %s' % version)
        tagging_info = None
        if not args.notag:
            tagging_info = dict(
                sign=args.sign or args.signingkey,
                signingkey=args.signingkey,
                message=args.message)
        release = gitflow.finish('hotfix', version,
                                 fetch=args.fetch, rebase=False,
                                 keep=args.keep, force_delete=False,
                                 tagging_info=tagging_info)

    #- publish
    @classmethod
    def register_publish(cls, parent):
        p = parent.add_parser('publish',
                help='Publish this hotfix branch to origin.')
        p.set_defaults(func=cls.run_publish)
        p.add_argument('version', nargs='?')

    @staticmethod
    def run_publish(args):
        gitflow = GitFlow()
        version = gitflow.name_or_current('hotfix', args.version)
        gitflow.start_transaction('publishing hotfix branch %s' % version)
        branch = gitflow.publish('hotfix', version)
        print
        print "Summary of actions:"
        print "- A new remote branch '%s' was created" % branch
        print "- The local branch '%s' was configured to track the remote branch" % branch
        print "- You are now on branch '%s'" % branch
        print


class SupportCommand(GitFlowCommand):
    @classmethod
    def register_parser(cls, parent):
        p = parent.add_parser('support', help='Manage your support branches.')
        p.add_argument('-v', '--verbose', action='store_true',
           help='Be verbose (more output).')
        sub = p.add_subparsers(title='Actions')
        cls.register_list(sub)
        cls.register_start(sub)

    #- list
    @classmethod
    def register_list(cls, parent):
        p = parent.add_parser('list',
                              help='Lists all existing support branches '
                              'in the local repository.')
        p.set_defaults(func=cls.run_list)
        p.add_argument('-v', '--verbose', action='store_true',
                help='Be verbose (more output).')

    @staticmethod
    def run_list(args):
        gitflow = GitFlow()
        gitflow.start_transaction()
        gitflow.list('support', 'version', use_tagname=True,
                     verbose=args.verbose)

    #- start
    @classmethod
    def register_start(cls, parent):
        p = parent.add_parser('start', help='Start a new support branch.')
        p.set_defaults(func=cls.run_start)
        p.add_argument('-F', '--fetch', action='store_true',
                help='Fetch from origin before performing local operation.')
        p.add_argument('name', action=NotEmpty)
        p.add_argument('base', nargs='?')

    @staticmethod
    def run_start(args):
        gitflow = GitFlow()
        # NB: `args.name` is required since the branch must not yet exist
        # :fixme: get default value for `base`
        gitflow.start_transaction('create support branch %s (from %s)' %
                (args.name, args.base))
        try:
            branch = gitflow.create('support', args.name, args.base,
                                    fetch=args.fetch)
        except (NotInitialized, BranchTypeExistsError, BaseNotOnBranch):
            # printed in main()
            raise
        except Exception, e:
            die("Could not create support branch %r" % args.name, e)
        print
        print "Summary of actions:"
        print "- A new branch", branch, "was created, based on", args.base
        print "- You are now on branch", branch
        print ""
