import os
import unittest
from areaCalculator import calculate_rectangle_area
from html_reporter import HTMLTestRunner  # Import the HTML runner

class TestRectangleArea(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(calculate_rectangle_area(5, 4), 20)
        self.assertEqual(calculate_rectangle_area(2.5, 3.5), 8.75)
        
    def test_zero_values(self):
        with self.assertRaises(ValueError):
            calculate_rectangle_area(0, 5)
        with self.assertRaises(ValueError):
            calculate_rectangle_area(5, 0)
            
    def test_negative_values(self):
        with self.assertRaises(ValueError):
            calculate_rectangle_area(-5, 4)
        with self.assertRaises(ValueError):
            calculate_rectangle_area(5, -4)

    def test_non_numeric_values(self):
        with self.assertRaises(TypeError):
            calculate_rectangle_area("5", 4)
        with self.assertRaises(TypeError):
            calculate_rectangle_area(5, "4")

if __name__ == '__main__':
    os.current_dir = os.path.dirname(os.path.abspath(__file__))
    # print(f"Current directory: {os.current_dir}")
    output_dir = os.path.join(os.current_dir, 'test-reports')
    os.makedirs(output_dir, exist_ok=True)

    # Swap out the default runner for the HTML reporter
    runner = HTMLTestRunner(
        report_filepath=os.path.join(output_dir, "test_report.html"),
        title="Application Unit Tests",
        description="Automated build verification report."
    )
    unittest.main(testRunner=runner)