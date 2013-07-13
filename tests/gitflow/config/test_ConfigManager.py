from os import path
from unittest2 import TestCase
from config.configmanager import ConfigManager
from tests.helpers import (copy_from_fixture, remote_clone_from_fixture,
                           all_commits, sandboxed, fake_commit)
from tests.helpers.factory import create_sandbox, create_git_repo
from const import CONFIG_VERSION, FLOW_DIR


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
        self._initRepo()

    @copy_from_fixture('blank_repo')
    def testInitializeFolder2(self):
        """
        just seeing if it will pass twice

        :return:
        """
        c = self._initRepo()
        
        #make sure the version number at least matches on the newly formed config file.
        self.assertEquals(c.systemConfig[CONFIG_VERSION], c.version)

    @copy_from_fixture('blank_repo')
    def testverifyGitIgnoreAdded(self):
        """
        We are ensuring that the gitignore file is being updated correctly
        :return:
        """
        c = self._initRepo()
        ignoreFilename = path.join(self.repo.workdir, '.gitignore')

        #if path.isfile(ignoreFilename):

        f = open(ignoreFilename, 'r')

        i = 0

        for line in f:
            if line == c.personalConfigFile:
                i += 1

        f.close()
        if i != 1:
            self.assertFalse(True)

        # now create another copy and make sure there is only one entry
        d = self._initRepo(True)

        f = open(ignoreFilename, 'r')

        i = 0

        for line in f:
            if line == c.personalConfigFile:
                i += 1

        if i != 1:
            self.assertFalse(True)

    def _initRepo(self, existing = False):
        # make sure the config folder doesn't exist
        flowdir = path.join(self.repo.workdir, '.flow')

        if not existing:
            # real quick, make sure nothing is there first
            self.assertFalse(path.isdir(flowdir))

        c = ConfigManager(self.repo)

        #now make sure the folder exists
        self.assertTrue(path.isdir(flowdir))
        return c