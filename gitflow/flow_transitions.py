__author__ = 'LID4EC9'

from flow_core import getParamString
import pprint


class BaseTransition():
    PARAM_START_BRANCH = 'startBranch'
    PARAM_GIT = 'git'
    PARAM_MERGE_INTO = 'mergeInto'
    PARAM_TARGET_BRANCH = 'targetBranch'
    TRANS_DEFAULT = False

    def __init__(self, params):
        self.startBranch = getParamString(params, self.PARAM_START_BRANCH, None)
        self.git = getParamString(params, self.PARAM_GIT, None)
        self.mergeInto = getParamString(params, self.PARAM_MERGE_INTO, None)
        self.targetBranch = getParamString(params, self.PARAM_TARGET_BRANCH, None)

    def runTransition(self, args):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        str_list = [self.__class__.__name__, "("]

        # This prints out the parameters for the transition
        for propertyName, value in vars(self).iteritems():
            if value is not None:
                str_list.append(propertyName + ": " + str(value) + ", ")

        str_list.append(")")

        return ''.join(str_list)


class transGup(BaseTransition):
    def runTransition(self, args):
        #git fetch origin && git rebase -p
        #git push -u bit --all
        #git push -u bit --tags
        print("ran transGup")
        pprint.pprint(args)


class transCreateBranch(BaseTransition):
    def runTransition(self, args):
        print("checkout -b {1} branch_develop")
        pprint.pprint(args)


class transFinish(BaseTransition):
    def runTransition(self, args):
        print("transFinish")
        pprint.pprint(args)


class transFail(BaseTransition):
    def runTransition(self, args):
        print("transFinish")
        pprint.pprint(args)


class transMergeBranch(BaseTransition):
    def runTransition(self, args):
        print("transMergeBranch")
        pprint.pprint(args)


class transGitCommand(BaseTransition):
    def runTransition(self, args):
        print("transGitCommand")
        pprint.pprint(args)


class transDeleteBranch(BaseTransition):
    def runTransition(self, args):
        print("transDeleteBranch")
        pprint.pprint(args)


class transPushToRemote(BaseTransition):
    def runTransition(self, args):
        print("transPushToRemote")
        pprint.pprint(args)


class TransitionFactory():
    @staticmethod
    def buildClass(trans, default, params):
        usingDefault = False

        if trans is None:
            usingDefault = True
            trans = default

        constructor = globals()[trans]
        instance = constructor(params)

        instance.TRANS_DEFAULT = usingDefault

        return instance