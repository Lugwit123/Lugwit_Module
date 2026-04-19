import unittest
from Lugwit_Module import *
from l_src.MayaToUe import  *

class TestGetExInfoFromDescriptionFile(unittest.TestCase):
    def test_getExInfoFromDescriptionFile(self):
        self.assertEqual(getExInfoFromDescriptionFile(), 'expected output')

if __name__ == '__main__':
    unittest.main()