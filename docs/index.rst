.. Git Flow Plus documentation master file, created by
   sphinx-quickstart on Thu Jul  4 02:25:07 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Git Flow Plus's documentation!
=========================================

Gitflow Plus is an attempt to add a workflow system to the source management system Git.  

Inception
================

The origins to Gitflow Plus can be traced to the original ``git flow``.  For the best introduction to get started with ``git flow``, please read Jeff Kreeftmeijer's blog post http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow.

Or have a look at one of these screen casts:

* `How to use a scalable Git branching model called git-flow
  <http://buildamodule.com/video/change-management-and-version-control-deploying-releases-features-and-fixes-with-git-how-to-use-a-scalable-git-branching-model-called-gitflow>`_
  (by Build a Module)

* `A short introduction to git-flow <http://vimeo.com/16018419>`_
  (by Mark Derricutt)

* `On the path with git-flow
  <http://codesherpas.com/screencasts/on_the_path_gitflow.mov>`_
  (by Dave Bock)

It is important to point out one important thing.  Gitflow Plus was never intended to be a fully secure, stringently enforced workflow system.  The incredibly flexible nature of Git prevents doing this.  Gitflow Plus is intended to be a short cute.  Think of the workflow paths as macros, you are fully capable of doing the exact same tasks manually, Gitflow Plus simply makes it easier.

Installing git-flow
====================

You can install ``git-flow``, using::

    easy_install gitflow

Or, if you'd like to use ``pip`` instead::

    pip install gitflow

``git-flow`` requires at least Python 2.5.

Integration with your shell
-----------------------------

For those who use the `Bash <http://www.gnu.org/software/bash/>`_ or `ZSH <http://www.zsh.org>`_ shell, please check out the excellent work on the `git-flow-completion <http://github.com/bobthecow/git-flow-completion>`_ project by `bobthecow <http://github.com/bobthecow>`_. It offers tab-completion for all git-flow subcommands and branch names.


Please help out
==================

This project is still under development. Feedback and suggestions are
very welcome and I encourage you to use the `Issues list
<http://github.com/htgoebel/gitflow/issues>`_ on Github to provide that
feedback.

Feel free to fork this repo and to commit your additions. For a list
of all contributors, please see the :file:`AUTHORS.txt`.

You will need :module:`unittest2` to run the tests.

History of the Project
=========================

gitflow was originally developed by Vincent Driessen as a set of
shell-scripts. In Juni 2007 he started a Python rewrite but did not
finish it. In February 2012 Hartmut Goebel started completing the
Python rewrite and asked Vincent to pull his changes. But in June 2012
Vincent closed the pull-request and deleted his ``python-rewrite``
branch. So Hartmut decided to release the Python rewrite on his own.

License terms
==================

git-flow is published under the liberal terms of the BSD License, see
the :file:`LICENSE.txt`. Although the BSD License does not
require you to share any modifications you make to the source code,
you are very much encouraged and invited to contribute back your
modifications to the community, preferably in a Github fork, of
course.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
