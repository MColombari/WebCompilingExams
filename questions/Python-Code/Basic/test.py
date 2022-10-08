[
  {
    "type": 3,
    "text": "Realizza una funzione \"run\" che sommi due numeri.",
    "options": """import unittest
from RunningFile import run


class Test(unittest.TestCase):
  def test_1(self):
    self.assertEqual(run(1, 2), 3, 'Errore')

  def test_2(self):
    self.assertEqual(run(0, 2), 2, 'Errore')

  def test_3(self):
    self.assertEqual(run(-1, 2), 1, 'Errore')


unittest.main()""",
    "correct_answer": "",
    "time_expected": 10
  },
  {
    "type": 3,
    "text": "Realizza una funzione \"run\" che moltiplichi due numeri.",
    "options": """import unittest
from RunningFile import run

class Test(unittest.TestCase):
  def test_1(self):
    self.assertEqual(run(1, 2), 2, 'Errore')
  def test_2(self):
    self.assertEqual(run(0, 2), 0, 'Errore')
  
  def test_3(self):
    self.assertEqual(run(-1, 2), -2, 'Errore')

unittest.main()""",
    "correct_answer": "",
    "time_expected": 10
  }
]