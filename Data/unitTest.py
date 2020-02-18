import unittest

import pytest
import timeout_decorator
import sys
sys.path.append('..')
from Data.mid import mid
from Data.FlagObj import Flag
class TestSum(unittest.TestCase):
    currentResult = None  # holds last result object passed to run method

    @classmethod
    def setResult(cls, amount, errors, failures, skipped):
        cls.amount, cls.errors, cls.failures, cls.skipped = \
            amount, errors, failures, skipped

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        self.setResult(amount, errors, failures, skipped)

    @classmethod
    def tearDownClass(cls):
        global flag
        flag = Flag(0)
        print("\ntests run: " + str(cls.amount))
        print("errors: " + str(len(cls.errors)))
        if len(cls.errors) != 0:
            flag.setRank(1)
        print("failures: " + str(len(cls.failures)))
        if len(cls.failures) != 0:
            flag.setRank(1)
        print("success: " + str(cls.amount - len(cls.errors) - len(cls.failures)))
        print("skipped: " + str(len(cls.skipped)))

    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method


    def test_sum_1(self):
        self.assertEqual(mid(3, 2), 1, "Should be 2")
    def test_sum_2(self):
        self.assertEqual(mid(5, 5), 5, "Should be 5")
    def test_sum_3(self):
        self.assertEqual(mid(3, 3), 3, "Should be 3")
    def test_sum_4(self):
        self.assertEqual(mid(5, 3), 1, "Should be 4")
    def test_sum_5(self):
        self.assertEqual(mid(2, 4), 2, "Should be 2")
    def test_sum(self):
        self.assertEqual(mid(0, 2), 1, "Should be 2")

class GetResult:
    def getResult(self):
        unittest.main(exit=False)
        return flag.getRank()
if __name__ == '__main__':
    r = GetResult()
    r.getResult()
    # unittest.main(exit=False)
    # print(flag.getRank())