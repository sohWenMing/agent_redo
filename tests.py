#!/usr/bin/env python3
import unittest
from functions import *

class TestFunction(unittest.TestCase):
    # def test_calculator_main(self):
    #     result = get_file_content("calculator", "main.py")
    #     print(result)
    # def test_calculator_pkg_main(self):
    #     result = get_file_content("calculator", "pkg/calculator.py")
    #     print(result)
    # def test_calculator_error_bin(self):
    #     result = get_file_content("calculator", "/bin")
    #     print(result)
    # def test_calculator_error_bin(self):
    #     result = get_file_content("calculator", "/bin/cat")
    #     print("result length: ", len(result))

    # def test_write_file_not_lorem(self):
    #     result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    #     print("result: ", result)
    # def test_write_file_more_lorem(self):
    #     result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    #     print("result: ", result)
    # def test_should_not_be_allowed(self):
    #     result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    #     print("result: ", result)

    def test_exec_file_1(self):
        result = run_python_file("calculator", ["main.py", "--verbose"])
        print("result1: ",result)
        result = run_python_file("calculator", "tests.py")
        print("result2: ",result)
        result = run_python_file("calculator", "../main.py")
        print("result3: ",result)
        result = run_python_file("calculator", "nonexistent.py")
        print("result4: ",result)


if __name__ == "__main__":
    unittest.main()
