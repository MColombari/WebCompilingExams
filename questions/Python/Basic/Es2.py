# -- "Easy", weight: '5'
# 'Realizza una funzione "run" '
# 'che moltiplichi due numeri.'

import unittest
from RunningFile import run


class Test(unittest.TestCase):
    def test_1(self):
        self.assertEqual(run(1, 2), 2, 'Errore')

    def test_2(self):
        self.assertEqual(run(0, 2), 0, 'Errore')

    def test_3(self):
        self.assertEqual(run(-1, 2), -2, 'Errore')


unittest.main()
