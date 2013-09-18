.. config:

====================
Gitflow Plus Workflow Configuration File
====================

-----------------------
Configuration Variables
-----------------------

To aid in building your workflow, several variables have been defined in the configuration system.  Feel free to use them wherever appropriate when building your workflow.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Development Branch Variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^
* To specify the development branch, you can use the variable ${branch_develop}
* To specify the master branch, you can use the variable ${branch_master}::


-----------------------
Configuration Settings
-----------------------
Used primarily for regression warnings.  All versions of GitFlow Plus are tested to the first version of the config file.  This setting allows the system to realize what version of GitFlow Plus was used to create the file and head off any incompatibilities::

    config_version=0.0.1

This is the name of master branch.  Best to think of this as your production branch.::

    branch_master=master

This is the develop branch.  All bug and feature branches start from here.  This is the branch that most development will be done on.::

    branch_develop=develop

These are the mainline branches in the system.  The important thing to note about these branches, are they are listed in the promotion order. Meaning, if a bug branch starts at develop, then must go thru Integration Testing, then Quality Assurance, then Production Assurance, then finally Production, the order this should be listed in would be:

develop,it,qa,pa,master



mainline_branches=${branch_develop},it,alpha,beta,${branch_master}

# Command branches can be thought of as the commands git flow plus uses.  For 
# example, if you define a command branch with the name 'bug' here, you would
# then be able to use the command:
# 'git flow bug start 123'
# Using the default workflow, that would create a branch called BUG_123 based
# off the develop branch.  This bug branch will follow the specified workflow
# the start is a command defined in the workflow configurations below.
command_branches={'bug', ${branch_develop}}, {'feature', ${branch_develop}}, {'hotfix', ${branch_master}}, 

# This flag will tell the system to automatically publish all new branches
# to the remote.  It is recommended to set this to prevent the possibility
# of developers stepping on each other
autopush_remotes=true

# This specifies the remote name to use for all remote work.  In all cases
# this can be overridden on the command line, but this is the default.
remote_name=origin

# ************ WORKFLOWS ************
# condition statements:
#   Condition statements take in a boolean value.  The codition statement
#   comes back with a boolean value.  That boolean value is checked against
#   the input parameter indicated in the workflow to determine if the check 
#   passed or not.  
#   for example:
#       branch_exist(true, false)
#   Say the above condition method returns true, indicating that the branch does
#   already exist.  The first parameter indicates if the condition is critical or
#   not.  Critical is defined as does the processing stop if the condition fails
#   The second parameter indicates that for the condition 
#   to pass, it must return false.  Therefore the condition would fail and
#   the workflow would stop.

#   condBranchExist(boolean, boolean) - Checks that the input branch exists or not
#   condIsClean(boolean, boolean) - Checks that the repo is clean or not.
#   condPushRemote(boolean, boolean) - 
#   condIsNextMaster(boolean, boolean)
#   condDefault() - If no condition is specified, this is the condition
#       that is run
#       Consists of:
#           condIsClean(true, true)

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
#                condFailNext= - the command to execute if condition fails, if
#                                   not included, will default to transError
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

