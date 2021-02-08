from django.test import TestCase

from app.calc import add

class CalcTests(TestCase):

    def test_add_numbers(self):
        """Tests that two numbers are added togheter"""

        self.assertEqual(add(1, 2), 3)
