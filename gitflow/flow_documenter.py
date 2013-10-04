__author__ = 'LID4EC9'

import gitflow


def printConfig(self):
    #indentText(indentLevel)
    print("")
    print(formatHeader("Base Variables:"))
    print(formatValuePair(self.CONFIG_VERSION, self.getConfigVersion()))
    print(formatValuePair(self.BRANCH_MASTER, self.getBranchMaster()))
    print(formatValuePair(self.BRANCH_DEVELOP, self.getBranchDevelop()))

    if self.getAutopushRemotes():
        print(formatValuePair(self.AUTOPUSH_REMOTES, "True"))
    else:
        print(formatValuePair(self.AUTOPUSH_REMOTES, "False"))

    print(formatValuePair(self.REMOTE_NAME, self.getRemoteName()))
    print("")
    print(formatHeader("Mainline Branches:"))

    for item in self.getMainlineBranches():
        print(indentText(1) + colorText(LIGHT_GREEN, item, COLOR_ENABLED))

    print("")
    print(formatHeader("Flow Commands:"))
    for item in self.getFlowCommands():
        print(str(item))