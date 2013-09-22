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

#from gitflow.core import GitFlow
from gitflow.util import itersubclasses
from gitflow.core import GitFlow
from gitflow.flow_exceptions import (GitflowError)
from gitflow.flow_commands import GitFlowCommand
from gitflow.flow_commands import DynamicCommand
from gitflow.config.configmanager import ConfigManager


__copyright__ = "2013 Willie Slepecki; Based on code written by: 2010-2011 Vincent Driessen; 2012-2013 Hartmut Goebel"
__license__ = "BSD"
__configFile__ = ".gitflow"


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
        cmd = DynamicCommand(dynamic, c)
        cmd.register_parser(placeholder)

    args = parser.parse_args()

    # Now run the specified command
    try:
        args.func(args)
    except KeyboardInterrupt:
        raise SystemExit('Aborted by user request.')

if __name__ == '__main__':
    try:
        main()
    except (GitflowError) as e:
        raise SystemExit('Error: %s' % e)
