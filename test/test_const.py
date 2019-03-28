import unittest
import lampy


class Equal42Test(unittest.TestCase):
    def runTest(self):
        self.assertEqual(42, lampy.const(42, 0))


class CurryingTest(unittest.TestCase):
    def runTest(self):
        x = lampy.const(42)
        self.assertTrue(x(0) == 42 and x(42) == 42)
