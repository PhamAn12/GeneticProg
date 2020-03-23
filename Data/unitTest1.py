import sys
sys.path.append('..')
from Variant.Pop2 import mid

import unittest


class TestSum(unittest.TestCase):
    currentResult = None  # holds last result object passed to run method


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
        self.assertEqual(mid(0, 2), 2, "Should be 2")

class GetResult:
    def getResult(self):
        import unittest
        unittest.main(exit=False)
        print("done")

if __name__ == '__main__':
    # r = GetResult()
    # r.getResult()
    unittest.main(exit=False)

# print("khabanh =)))")