#!/usr/bin/env python
"""
git-flow

.. program:: git flow

.. cmdoption:: -v, --verbose

       Produce more output.

.. cmdoption:: -h, --help

       Print usage, help and information on the available commands.

"""
#
# This file is part of `gitflow`.
# Copyright (c) 2010-2011 Vincent Driessen
# Copyright (c) 2012-2013 Hartmut Goebel
# Distributed under a BSD-like license. For full terms see the file LICENSE.txt
#

import argparse
import sys
#from gitflow.core import GitFlow
from gitflow.util import itersubclasses
from gitflow.core import GitFlow
from gitflow.flow_exceptions import (GitflowError)
from gitflow.flow_commands import GitFlowCommand
from gitflow.flow_config import ConfigManager


__copyright__ = "2013 Willie Slepecki; Based on code written by: 2010-2011 Vincent Driessen; 2012-2013 Hartmut Goebel"
__license__ = "BSD"
__configFile__ = ".gitflow"

if sys.version_info < (2, 7):
    raise "must use python 2.7 or greater"


def die(*texts):
    raise SystemExit('\n'.join(map(str, texts)))


class NotEmpty(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            raise argparse.ArgumentError(self, 'must not by empty.')
        setattr(namespace, self.dest, values)


def main():
    parser = argparse.ArgumentParser(prog='git flow')
    placeholder = parser.add_subparsers(title='Subcommands')

    # This initializes the built in commands
    for cls in itersubclasses(GitFlowCommand):
        cls.register_parser(placeholder)

    c = ConfigManager(GitFlow())

    # This initializes the dynamic commands.
    for dynamic in c.getFlowCommands():
        initcmdmsg = dynamic.workflow.description
        p = placeholder.add_parser(dynamic.flowCommand, help=initcmdmsg)
        sub = p.add_subparsers(title='Actions')
        #p.set_defaults(func=self.run)

        if len(dynamic.workflow.subCommands) > 0:
            # we have multiple actions, lets add them
            for action in dynamic.workflow.subCommands:
                psub = sub.add_parser(action.subName,
                                      help=c.resolveConfig(action.usageHelp, dynamic.flowCommand))

                # psub.set_defaults(func=self.run)

                for option in action.options:
                    psub.add_argument(option.option, action='store_true', help=option.description)

                for tmpArg in action.args:
                    psub.add_argument(tmpArg.arg, action=NotEmpty, help=tmpArg.description)

    args = parser.parse_args()

    # Now run the specified command
    try:
        print("running the command")
        # print(sys.argv[1])
        # print(sys.argv[2])
        #pprint(str(args))
        args.func(args)
    except KeyboardInterrupt:
        raise SystemExit('Aborted by user request.')


if __name__ == '__main__':
    try:
        main()
    except (GitflowError) as e:
        raise SystemExit('Error: %s' % e)
