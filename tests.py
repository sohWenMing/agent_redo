import unittest
from functions import *

class TestFunction(unittest.TestCase):
    def test_calculator_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)
    def test_calculator_pkg_main(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
    def test_calculator_error_bin(self):
        result = get_file_content("calculator", "/bin")
        print(result)
    def test_calculator_error_bin(self):
        result = get_file_content("calculator", "/bin/cat")
        print("result length: ", len(result))

if __name__ == "__main__":
    unittest.main()
