__author__ = 'scphantm'

from os import path
from unittest2 import TestCase
from config.configmanager import ConfigManager
from tests.helpers import (copy_from_fixture, remote_clone_from_fixture,
                           all_commits, sandboxed, fake_commit)
from tests.helpers.factory import create_sandbox, create_git_repo
from const import CONFIG_VERSION


class TestGitFlowBasics(TestCase):
    """
    Test cases that run the config manager thru its pases
    """
    @copy_from_fixture('blank_repo')
    def test_version_number_calculator(self):
        """
        Test that ensures the version calculator is running properly
        :return:
        """
        c = ConfigManager(self.repo)

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

    @copy_from_fixture('blank_repo')
    def testInitializeFolder(self):
        """
        This will test that the system can create a new folder in the
        repo and create the defalut folders in it

        :return:
        """
        # make sure the config folder doesn't exist
        flowdir = path.join(self.repo.workdir, '.flow')

        # real quick, make sure nothing is there first
        self.assertFalse(path.isdir(flowdir))

        c = ConfigManager(self.repo)

        #now make sure the folder exists
        self.assertTrue(path.isdir(flowdir))

    @copy_from_fixture('blank_repo')
    def testInitializeFolder2(self):
        """
        just seeing if it will pass twice

        :return:
        """
        flowdir = path.join(self.repo.workdir, '.flow')

        # make sure the config folder doesn't exist
        self.assertFalse(path.isdir(flowdir))

        c = ConfigManager(self.repo)

        #now make sure the folder exists
        self.assertTrue(path.isdir(flowdir))
        
        #make sure the version number at least matches on the newly formed config file.
        self.assertEquals(c.systemConfig[CONFIG_VERSION], c.version)