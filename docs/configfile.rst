.. _configFile:

******************************************
Gitflow Plus Workflow Configuration System
******************************************

.. index:: config, configuration, workflow

Configuration Overview
======================

Gitflow Plus has a flexible configuration system.  One problem common to Git workflow systems is a byproduct of the power of Git itself, its distributed nature.  Because the basic design of Git relies on the fact there are no central servers, it is nearly impossible to enforce a full workflow system.  To get around this problem, Gitflow Plus employes a simple configuration system.  When a repository is initialized in the Gitflow Plus system, a new folder named ``.flow`` is created in the project's root.  This folder has the configuration file for Gitflow Plus.  This way, the workflow configuration can be simply committed to the repository and distributed to the other developers on your team.

The configuration file of Gitflow Plus is created in the ``.flow`` folder and named ``gitflowplus.flowini``.  This file can be committed to the repository and then shared with all other developers on your project easily.

Configuration Variables
=======================

To aid in building your workflow, several variables have been defined in the configuration system.  Feel free to use them wherever appropriate when building your workflow.

:data:`${branch_develop}` - Variable for the Development Branch.  Gets its value from the ``branch_develop`` configuration setting.

:data:`${branch_master}` - Variable for the Master Branch.  Gets its value from the ``branch_master`` configuration setting.


Configuration Settings
======================

config_version
--------------
Used primarily for regression warnings.  All versions of GitFlow Plus are tested to the first version of the config file.  This setting allows the system to realize what version of GitFlow Plus was used to create the file and head off any incompatibilities::

    config_version=0.0.1

branch_master
-------------
This is the name of master branch.  Best to think of this as your production branch.::

    branch_master=master

branch_develop
--------------
This is the develop branch.  This is the primary branch the developers should be working in.  This is the branch that most development will be done on.::

    branch_develop=develop

mainline_branches
-----------------
These are the mainline branches in the system.  The single most important thing to note about this setting is the branches must be listed in the promotion order. Meaning, if a bug branch starts at develop, then must go thru Integration Testing, then Quality Assurance, then Production Assurance, then finally Production, then the setting may look like this::

    mainline_branches=${branch_develop},it,qa,pa,${branch_master}

Another possibility is a bit more traditional (i refuse to say old) way of referring to a development cycle::

    mainline_branches=${branch_develop},it,alpha,beta,${branch_master}

command_branches
----------------
Command branches can be thought of as the commands GitFlow Plus uses.  For example, if you define a command branch with the name ``bug`` here, you would then be able to use the command: ``git flow bug start 123`` (assuming your using the default workflow file), that would create a branch called BUG_123 based off the develop branch.  This bug branch will follow the specified workflow the start is a command defined in the workflow configurations below.::

    command_branches={'bug', ${branch_develop}}, {'feature', ${branch_develop}}, {'hotfix', ${branch_master}}

autopush_remotes
----------------
This flag will tell the system to automatically publish all new branches to the remote.  It is recommended to set this to prevent the possibility of developers stepping on each other.

Legal values: ``true``, ``false``::

    autopush_remotes=true

remote_name
-----------
This specifies the remote name to use for all remote work.  In all cases this can be overridden on the command line, but this is the default.

If this flag is set to a remote that doesn't exist, an error will be thrown and Gitflow Plus will stop execution.::

    remote_name=origin

Workflows
=========

Here is described all the elements of the workflow system and how to pull them together into a single coherent workflow for your project.

Condition Statements
--------------------

Condition statements can be thought of as a yes or no question to be asked before performing a transition.  Each condition statement is written into Gitflow Plus's core API's.  These API's are flexible in the fact that you can determine thru parameters what constitutes the answer you are looking for.  

For example, say you wanted to verify that a branch does not exist before you do an operation, say creating a new branch.  You could set the condition statement to::

    condBranchNotExist

and be done with it.  But say in the next step, you want to verify that the branch was actually created before you moved on to the next transition.  Well now, Gitflow Plus would have to create a second condition like this::

    condBranchExist

for you to do your check.  This leads to a bloated API, so we introduced the first parameter for the condition, ``valid``.  This is a ``true``, or ``false`` value that is passed in to specify the result you are looking for.  So in the above example, instead of two different methods, you can use::

    condBranchExist(false)

for the first step.  This is saying in essence, I expect the branch to not exist.  Then in your second step, you could use::

    condBranchExist(true)

Here, you are saying you do expect the branch to exist.

One aspect of a complex workflow is many times, the answer you are looking for is not a simple yes or no, there can be subtle shades of gray.  Meaning, you can encounter situations where just because something failed, doesn't mean that its a critical failure that should stop processing, it could be a check where if it fails, you would want a second transition executed instead of the primary transition of the task, or you may want to simply print on the screen that something isn't right, then continue anyways.  Think of it as a warning.

For this reason, a second parameter is added to each condition statement.  Again its a boolean, but it indicates to the workflow system whether the failure of a certain check is critical or not.  Like this::

    condBranchExist(true, true)

Above is stating that you expect the branch to be there, and if it isn't there, that is a critical error and execute the transition indicated by the setting ``condCriticalFailNext`` in the workflow step.  But, if it where::

    condBranchExist(true, false)

Then this would say that if the branch doesn't exist, its a non-critical error and execute the transition indicated in the ``condNonCriticalFailNext`` configuration setting, otherwise, if you specified::

    condBranchExist(true, true)

This statement would say that if the branch doesn't exist, it is a critical error and execute the transition indicated in the ``condCriticalFailNext`` configuration setting.


condBranchExist
^^^^^^^^^^^^^^^
.. method:: condBranchExist(valid, critical)

    | Params:
    | ``valid`` (:data:`boolean`): Sets whether a success would be considered a true or false
    | ``critical`` (:data:`boolean`): Tells if the condition is critical or not

    Checks whether the target branch about to be created or worked on exists or not.

condIsClean
^^^^^^^^^^^
.. method:: condIsClean(valid, critical)

    | Params:
    | ``valid`` (:data:`boolean`): Sets whether a success would be considered a true or false
    | ``critical`` (:data:`boolean`): Tells if the condition is critical or not

    Checks whether the Git repository is clean or not

condPushRemote
^^^^^^^^^^^^^^
.. method:: condPushRemote(valid, critical)

    | Params:
    | ``valid`` (:data:`boolean`): Sets whether a success would be considered a true or false
    | ``critical`` (:data:`boolean`): Tells if the condition is critical or not

    Returns the value of the configuration setting ``autopush_remotes``.  This will allow you to build workflow sequences and decide whether or not to push newly created branches to the configured remote.

condIsNextMaster
^^^^^^^^^^^^^^^^
.. method:: condIsNextMaster(valid, critical)

    | Params:
    | ``valid`` (:data:`boolean`): Sets whether a success would be considered a true or false
    | ``critical`` (:data:`boolean`): Tells if the condition is critical or not

    Returns whether or not the next branch in the branch chain is master or not.  This is here because  one may want to build their workflows in such a way where the only way to promote a branch to production (master) is thru a release branch.  This can be used to prevent, or allow that.

condDefault
^^^^^^^^^^^
.. method:: condDefault(valid, critical)

    | Params:
    | ``valid`` (:data:`boolean`): Sets whether a success would be considered a true or false
    | ``critical`` (:data:`boolean`): Tells if the condition is critical or not

    In your workflow, if you don't specify a condition, this is run by default.  This default condition consits of a chain of the frequently used conditions.  This method chains ``condIsClean`` and ``condIsNextMaster`` both set with ``(true, true)`` parameters.

Transition Commands
-------------------


# Predefined Steps
#   trans_finish - Finishes off the transaction by displaying the steps that was done
#   transError - rolls back the transaction and displays the errors.  If any 
#       commits occured, it will rebase them out and return it to the previous
#       state
#   trans_gup - this does a fetch/rebase instead of a pull.  A pull creates a new commit
#       for the branch, this does not.  This keeps the commit tree clean in comparison
#       This is only done if there is a remote configured

# Transition Commands
#   transCreateBranch(newBranch, branchFrom)
#       Throws errors if:
#           The newBranch doesn't exist yet.
#           The repo is dirty.
#   transCheckoutBranch(branch)
#   transtransMergeBranch(fromBranch, intoBranch)
#   transDeleteBranch(branch)
#   transGitCommand(gitcommand)
#   transPushToRemote()
#   transError()
#   transFinish()
#   transGup()
# http://manual.macromates.com/en/language_grammars
# http://www.sublimetext.com/forum/viewtopic.php?f=3&t=6381
# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=18&cad=rja&ved=0CGYQFjAHOAo&url=https%3A%2F%2Fdocs.google.com%2Fdocument%2Fd%2F1jPflAMP-HT1594MQWwcipEJekrmRBoHyTU2YLtmwMLM%2Fedit%3Fusp%3Dsharing&ei=NYQ4UpzGEKfD4AO1jICwCQ&usg=AFQjCNFRQBs-op3Vjl4TK2Ape-A71Oo_CA&sig2=wlO9NVR77SwEJf8zjI_JTw


# [workflows] - This indicates the workflow begins here.  There can be only one workflow statement
#    [[command]]
#        [[[subcommand]]]
#            [[[[steps]]]]
#                condition= - the condition to check before transition, if
#                                   not included, will default to condDefault
#                condCriticalFailNext= - the command to execute if condition fails, if
#                                   not included, will default to transError
#                condNonCriticalFailNext - 
#                transition= - the command to be executed if the condition passes
#                transFailNext= - the command to execute if transition fails, if
#                                   not included, will default to transError
[workflows]
    [[gup]]
        description=This is the gup that does a fetch/rebase instead of a pull
        [[[default]]]
            [[[[step1]]]]
                condition=
                transition=transGup('bla')

    [[command_{0}]]
        description=This is the first
        [[[start]]]
            [[[[step1]]]]
                transition=trans_gup

            [[[[step2]]]]
                condition=condBranchExist(true, false)
                transition=transCreateBranch(checkout -b {1} branch_develop)
            [[[[step3]]]]
                condition=condPushRemote(true, true)
                condFailNext=transFinish()
                transition=transPushToRemote(push <remote-name> <branch-name>)
        [[[next]]]
            [[[[step1]]]]${branch_develop},it,alpha,beta,${branch_master}
                condition=condDefault(),condIsNextMaster(true, true)
                transition=transMergeBranch(${branch_develop})
            [[[[step2]]]]
                transition=transMergeBranch(${branch_next})
            [[[[step3]]]]
                transition=transGitCommand(checkout -b {1} branch_develop)
            [[[[step4]]]]
                transition=transDeleteBranch(branch)
            [[[[step5]]]]
                transition=transPushToRemote(push <remote-name> <branch-name>)
    [[command_hotfix]]
        [[[start]]]
            [[[[step1]]]]
                transition=trans_gup
            [[[[step2]]]]
                condition=condBranchExist(true, false)
                transition=transCreateBranch(checkout -b {1} branch_develop)
            [[[[step3]]]]
                condition=condPushRemote(true, true)
                transition=transPushToRemote(push <remote-name> <branch-name>)
        [[[finish]]]
            [[[[step1]]]]
                transition=transMergeBranch
            [[[[step2]]]]
                transition=transGitCommand(checkout -b {1} branch_develop)
            [[[[step3]]]]
                transition=transDeleteBranch(branch)
            [[[[step4]]]]
                transition=transPushToRemote(push <remote-name> <branch-name>)
    [[release]]
        description=This creates releases to move groups thru the workflows
        [[[start]]]
            [[[[step1]]]]
                transition=checkout -b release-1.2 develop

