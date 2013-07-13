__author__ = 'scphantm'

from flow_exceptions import ConstError


class _const:
    """
    this class implements immutable constants.  This is to prevent people
    from accidently reimplementing constant names
    """

    def __setattr__(self, name, value):
        """
        Internal attribute setter that allows items to be implemented once but
        not be reimplemented twice.
        :param name:
        :param value:
        :raise:
        """
        if self.__dict__.has_key(name):
            raise ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value


import sys

sys.modules[__name__] = _const()

import const

# configuration constants
const.CONFIG_VERSION = "config_version"
const.BRANCH_MASTER = 'branch_master'
const.BRANCH_DEVELOP = 'branch_develop'
const.MAINLINE_BRANCHES = 'mainline_branches'

const.REMOTE_ORIGIN = 'remote_origin'

# These are configuration values
const.FLOW_DIR = '.flow'

const.SYS_CONFIG_FILE = 'gitflowplus.ini'
const.PERC_CONFIG_FILE = 'personal.ini'
