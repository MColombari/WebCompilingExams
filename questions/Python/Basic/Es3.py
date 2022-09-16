# -- "Normal", weight: '50'
# 'Realizza una funzione "run" '
# 'che sottragga il primo con il secondo.'
# '********************** '
# '********************** '
# '********************** '
# '********************** '
# '********************** '
# '********************** '
# '********************** '

import unittest
from RunningFile import run


class Test(unittest.TestCase):
    def test_1(self):
        self.assertEqual(run(1, 2), -1, 'Errore')

    def test_2(self):
        self.assertEqual(run(0, 2), -2, 'Errore')

    def test_3(self):
        self.assertEqual(run(-1, 2), -3, 'Errore')

    def test_4(self):
        self.assertEqual(run(5, 2), 3, 'Errore')

    def test_5(self):
        self.assertEqual(run(100, 99), 1, 'Errore')


unittest.main()
