import unittest
from calculateDivision import calculateDivision

class TestCalculateDivision(unittest.TestCase):
    def test_division(self):
        self.assertEqual(calculateDivision(10, 2), "The result of the division is: 5.0")
        self.assertEqual(calculateDivision(7, 3), "The result of the division is: 2.3333333333333335")
    
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculateDivision(10, 0)
    
    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            calculateDivision("10", 2)
        with self.assertRaises(TypeError):
            calculateDivision(10, "2")

if __name__ == "__main__":
    unittest.main()