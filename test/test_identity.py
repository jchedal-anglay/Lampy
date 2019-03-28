import unittest
import lampy


class IdentityTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual([], lampy.identity([]))
        self.assertEqual((), lampy.identity(()))
        self.assertEqual(4, lampy.identity(4))
