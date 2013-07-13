#
# This file is part of `gitflow`.
# Copyright (c) 2010-2011 Vincent Driessen
# Copyright (c) 2012-2013 Hartmut Goebel
# Distributed under a BSD-like license. For full terms see the file LICENSE.txt
#

__copyright__ = "2010-2011 Vincent Driessen; 2012-2013 Hartmut Goebel"
__license__ = "BSD"
"""
This file contains all excpetions for the system.  We are putting everything here
simply to make the code easier to navigate
"""


class GitflowError(Exception):
    """
    This object is created like this to keep your try statements as easy as possible
    if the exception that you get in your try statement is a derivative of GitFlowError,
    you are assured that it is a Git Flow Plus application error and not some exception
    thrown by a library or python itself
    """
    pass


class ObjectError(GitflowError):
    """
    The is a base object error.  This base object indicates that exceptions is because
    an object was expected and not recieved, wasn't initialized, or was in some other way
    dirty.
    """
    pass


class StateError(GitflowError):
    """
    Base object error for the work flow system to indicate something was wrong with the state
    """
    pass


class ConstError(GitflowError):
    """
    This indicates that someone has tried to set the value of a constant twice.
    """
    pass


class WorkflowInitializationError(StateError):
    """
    indicates that the workflow system hasn't been issued a start state
    """
    pass


"""
class Usage(GitflowError):
    def __str__(self):
        return '\n'.join(map(str, self.args))


class OperationsError(GitflowError):
    pass


class PrefixNotUniqueError(OperationsError):
    pass


class MergeError(OperationsError):
    pass


class StatusError(GitflowError):
    pass


class WorkdirIsDirtyError(StatusError):
    pass


class NotInitialized(StatusError):
    pass


class AlreadyInitialized(StatusError):
    def __str__(self):
        return ("Already initialized for gitflow.\n"
                "To force reinitialization use: git flow init -f")


class MergeConflict(StatusError):
    def __str__(self):
        return '\n'.join([
            "Merge conflicts not resolved yet, use:",
            "    git mergetool",
            "    git commit",
        ])





class BadObjectError(ObjectError):
    pass


class NoSuchBranchError(ObjectError):
    pass


class NoSuchRemoteError(ObjectError):
    pass


class BaseNotOnBranch(ObjectError):
    def __str__(self):
        return ("Given base '%s' is not a valid commit on '%s'."
                % (self.args[1], self.args[0]))


class BranchExistsError(ObjectError):
    pass


class TagExistsError(ObjectError):
    pass


class BranchTypeExistsError(ObjectError):
    def __str__(self):
        return ("There is an existing %s branch. "
                "Finish that one first." % self.args[0])


class NoSuchLocalBranchError(NoSuchBranchError):
    def __str__(self):
        return "Local branch '%s' does not exist." % self.args[0]
"""

"""
Configuration Manager Exceptions
"""


class NoRepositoryObject(ObjectError):
    """
    This is thrown indicating when an instance of the working repository was expected
    and was not given
    """
    pass