import unittest
from functions import *

class TestFunction(unittest.TestCase):
    def test_calculator_root_folder(self):
        result = get_files_info("calculator", ".")
        print(result)
    def test_calculator_root_pkg(self):
        result = get_files_info("calculator", "pkg")
        print(result)
    def test_calculator_error_bin(self):
        result = get_files_info("calculator", "/bin")
        print(result)
    def test_error_outer_dir(self):
        result = get_files_info("calculator", "../")
        print(result)

if __name__ == "__main__":
    unittest.main()
