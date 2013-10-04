__author__ = 'LID4EC9'

from flow_core import GitflowCoreCommands
import pprint


class BaseTransition(GitflowCoreCommands):
    PARAM_START_BRANCH = 'startBranch'
    PARAM_GIT = 'git'
    PARAM_MERGE_INTO = 'mergeInto'
    PARAM_TARGET_BRANCH = 'targetBranch'

    def __init__(self, params):
        self.startBranch = self._procParamString(params, self.PARAM_START_BRANCH, None)
        self.git = self._procParamString(params, self.PARAM_GIT, None)
        self.mergeInto = self._procParamString(params, self.PARAM_MERGE_INTO, None)
        self.targetBranch = self._procParamString(params, self.PARAM_TARGET_BRANCH, None)

    def runTransition(self):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        str_list = ["        " + self.__class__.__name__ + "\n"]

        # This prints out the parameters for the transition
        for propertyName, value in vars(self).iteritems():
            if value is not None:
                str_list.append("          " + propertyName + ": " + value + "\n")

        return ''.join(str_list)


class transGup(BaseTransition):
    def runTransition(self):
        #git fetch origin && git rebase -p
        #git push -u bit --all
        #git push -u bit --tags
        print("ran transGup")


class transCreateBranch(BaseTransition):
    def runTransition(self):
        print("checkout -b {1} branch_develop")


class transFinish(BaseTransition):
    def runTransition(self):
        print("transFinish")


class transFail(BaseTransition):
    def runTransition(self):
        print("transFinish")


class transMergeBranch(BaseTransition):
    def runTransition(self):
        print("transMergeBranch")


class transGitCommand(BaseTransition):
    def runTransition(self):
        print("transGitCommand")


class transDeleteBranch(BaseTransition):
    def runTransition(self):
        print("transDeleteBranch")


class transPushToRemote(BaseTransition):
    def runTransition(self):
        print("transPushToRemote")


class TransitionFactory():
    @staticmethod
    def buildClass(trans, default, params):
        if trans is None:
            trans = default

        constructor = globals()[trans]
        instance = constructor(params)
        return instance