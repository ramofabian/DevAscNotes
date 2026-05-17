#test_mathy.py
import os
import unittest
from mathy import add_numbers
from html_reporter import HTMLTestRunner  # Import the HTML runner
import xmlrunner  # Import the XML runner

class TestAddNumbers(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(3, 4), 7, "Should be 7 when adding 3 and 4")
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-3, -4), -7, "Should be -7 when adding -3 and -4")
    
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(3, -4), -1, "Should be -1 when adding 3 and -4")

    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 5), 5, "Should be 5 when adding 0 and 5")
        self.assertEqual(add_numbers(5, 0), 5, "Should be 5 when adding 5 and 0")

    def test_add_strings(self):
        with self.assertRaises(TypeError):
            add_numbers("3", "4")

if __name__ == "__main__":
    os.current_dir = os.path.dirname(os.path.abspath(__file__))
    # print(f"Current directory: {os.current_dir}")
    output_dir = os.path.join(os.current_dir, 'test-reports')
    os.makedirs(output_dir, exist_ok=True)
       
    # Simple test runner
    unittest.main()


    # # Swap out the default runner for the HTML reporter
    # runner = HTMLTestRunner(
    #     report_filepath=os.path.join(output_dir, "test_report.html"),
    #     title="Application Unit Tests",
    #     description="Automated build verification report."
    # )
    # unittest.main(testRunner=runner)

    # # Results will be saved as XML inside the 'test-reports' directory
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output_dir))

