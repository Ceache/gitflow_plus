__author__ = 'scphantm'

from unittest2 import TestCase
from conf.configmanager import ConfigManager
from tests.helpers import (copy_from_fixture, remote_clone_from_fixture,
                           all_commits, sandboxed, fake_commit)
from tests.helpers.factory import create_sandbox, create_git_repo


class TestGitFlowBasics(TestCase):
    """
    Test cases that run the config manager thru its pases
    """

    def test_version_number_calculator(self):
        """
        Test that ensures the version calculator is running properly
        :return:
        """
        c = ConfigManager()

        self.assertEquals(c._compareVersion('2.0.0', '1.0.0'), 1)
        self.assertEquals(c._compareVersion('1.0.0', '2.0.0'), -1)
        self.assertEquals(c._compareVersion('1.0.0', '1.0.0'), 0)
        self.assertEquals(c._compareVersion('12.01.0', '12.1.0'), 0)
        self.assertEquals(c._compareVersion('13.0.1', '13.00.02'), -1)
        self.assertEquals(c._compareVersion('1.1.1', '1.1.1'), 0)
        self.assertEquals(c._compareVersion('1.1.2', '1.1.1'), 1)
        self.assertEquals(c._compareVersion('1.1.3', '1.1.3'), 0)
        self.assertEquals(c._compareVersion('3.1.1', '3.1.2'), -1)
        self.assertEquals(c._compareVersion('1.1.0', '1.10.0'), -1)

    @copy_from_fixture('sample_repo')
    def testInitializeFolder(self):
        pass