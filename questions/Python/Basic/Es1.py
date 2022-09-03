"""Easy - Realizza una funzione 'run' che sommi due numeri. """

import unittest
from RunningFile import run


class Test(unittest.TestCase):
    def test_1(self, path=None):
        self.assertEqual(run(1, 2), 3, 'Errore')

    def test_2(self, path=None):
        self.assertEqual(run(0, 2), 2, 'Errore')

    def test_3(self, path=None):
        self.assertEqual(run(-1, 2), 1, 'Errore')


unittest.main()
