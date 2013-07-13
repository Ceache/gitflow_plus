"""
git-flow -- A collection of Git extensions to provide high-level
repository operations for Vincent Driessen's branching model.
"""
#
# This file is part of `gitflow`.
# Copyright (c) 2010-2011 Vincent Driessen
# Copyright (c) 2012-2013 Hartmut Goebel
# Distributed under a BSD-like license. For full terms see the file LICENSE.txt
#

VERSION = (0, 0, 1, 'dev')
import gitflow.bin

__version__ = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__author__ = "Willie Slepecki, Hartmut Goebel, Vincent Driessen"
__contact__ = "scphantm@gmail.com"
__homepage__ = "https://github.com/scphantm/gitflow_plus.git"
__docformat__ = "restructuredtext"
__copyright__ = "2013 Willie Slepecki; Based on code written by: 2010-2011 Vincent Driessen; 2012-2013 Hartmut Goebel"
__license__ = "BSD"
