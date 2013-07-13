#
# Shamelessly ripped from
# http://code.activestate.com/recipes/576949-find-all-subclasses-of-a-given-class/
#
def itersubclasses(cls, _seen=None):
    """
    itersubclasses(cls)

    Generator over all subclasses of a given class, in depth first order.

    >>> list(itersubclasses(int)) == [bool]
    True
    >>> class A(object): pass
    >>> class B(A): pass
    >>> class C(A): pass
    >>> class D(B,C): pass
    >>> class E(D): pass
    >>>
    >>> for cls in itersubclasses(A):
    ...     print(cls.__name__)
    B
    D
    E
    C
    >>> # get ALL (new-style) classes currently defined
    >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
    ['type', ...'tuple', ...]
    """

    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
                        'new-style classes, not %.100r' % cls)
    if _seen is None: _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError: # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub


class StringFormatter:
    BLUE = "\033[0;34m"
    LIGHT_BLUE = "\033[1;34m"
    GREEN = "\033[0;32m"
    CYAN = "\033[0;36m"
    PURPLE = "\033[0;35m"
    BROWN = "\033[0;33m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_GREEN = "\033[1;32m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_PURPLE = "\033[1;35m"
    YELLOW = "\033[1;33m"
    WHITE = "\033[1;37m"
    RED = "\033[0;31m"
    ENDC = "\033[0;0m"
    #def __init__(self):

    def colorText(self, color, text):
        return color + text + self.ENDC

    def printColorText(self, color, text):
        print(color + text + self.ENDC)

    def to_bool(self, bool_str):
        """Parse the string and return the boolean value encoded or raise an exception"""
        if isinstance(bool_str, basestring) and bool_str:
            if bool_str.lower() in ['true', 't', '1']:
                return True
            elif bool_str.lower() in ['false', 'f', '0']:
                return False

        #if here we couldn't parse it
        raise ValueError("%s is no recognized as a boolean value" % bool_str)