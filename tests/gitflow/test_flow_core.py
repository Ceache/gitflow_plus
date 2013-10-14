__author__ = 'lid4ec9'

from unittest2 import TestCase
from gitflow.flow_core import (boolToString,
                               stringToBool,
                               getParamBool,
                               getParamString)


class TestFlowCore(TestCase):

    def test_getParamString(self):
        """
            tests the retrieving of a parameter as a boolean.
            """
        tst = {'testTrue': "true", "testFalse": "false"}

        self.assertEqual(getParamString(tst, "testTrue"), "true")
        self.assertEqual(getParamString(tst, "testFalse"), "false")
        self.assertEqual(getParamString(tst, "desntexist"), None)
        self.assertEqual(getParamString(tst, "desntexist", "true"), "true")
        self.assertEqual(getParamString(tst, "desntexist", "false"), "false")

    def test_getParamBool(self):
        """
        tests the retrieving of a parameter as a boolean.
        """
        tst = {'testTrue': "true", "testFalse": "false"}

        self.assertEqual(getParamBool(tst, "testTrue"), True)
        self.assertEqual(getParamBool(tst, "testFalse"), False)
        self.assertEqual(getParamBool(tst, "desntexist"), None)
        self.assertEqual(getParamBool(tst, "desntexist", True), True)
        self.assertEqual(getParamBool(tst, "desntexist", False), False)

    def test_boolToString(self):
        """
        Tests the bool to string method
        """
        self.assertEqual(boolToString(True), "True")
        self.assertEqual(boolToString(False), "False")

        self.assertRaises(ValueError, boolToString, None)

    def test_stringToBool(self):
        """
        Tests the various ways that strings could be converted into booleans
        """
        self.assertEqual(stringToBool("True"), True)
        self.assertEqual(stringToBool("true"), True)
        self.assertEqual(stringToBool("TRUE"), True)
        self.assertEqual(stringToBool("1"), True)
        self.assertEqual(stringToBool("T"), True)
        self.assertEqual(stringToBool("t"), True)
        self.assertEqual(stringToBool("yes"), True)
        self.assertEqual(stringToBool("False"), False)
        self.assertEqual(stringToBool("false"), False)
        self.assertEqual(stringToBool("FALSE"), False)
        self.assertEqual(stringToBool("0"), False)
        self.assertEqual(stringToBool("F"), False)
        self.assertEqual(stringToBool("f"), False)
        self.assertEqual(stringToBool("no"), False)

        self.assertRaises(ValueError, stringToBool, None)
