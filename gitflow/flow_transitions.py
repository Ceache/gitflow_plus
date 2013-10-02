__author__ = 'LID4EC9'


class BaseTransition(object):

    def runTransition(self):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        str_list = ["        Transition: " + self.__class__.__name__ + "\n"]
        return ''.join(str_list)


class transGup(BaseTransition):
    def runTransition(self):
        print("ran transGup")


class TransitionFactory():
    @staticmethod
    def buildClass(condition):
        constructor = globals()[condition]
        instance = constructor()
        return instance