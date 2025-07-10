import unittest
from functions import get_files_info, get_file_content
import os
from config import agent_config

class TestFunctions(unittest.TestCase):
    def test_get_files_info(self):
        
        class Test():
            def __init__(self,
                         working_directory,
                         directory,
                         isExpectErr,
                         expectedErrMsg):
                self.working_directory = working_directory
                self.directory = directory
                self.isExpectErr = isExpectErr
                self.expectedErrMsg = expectedErrMsg

        tests = [
            Test(".", "../", True, 
                    f'Error: Cannot list "../" as it is outside the permitted working directory'),
            Test(".", None, False, None),
            Test(".", "functions.py", True, 
                 f'Error: "functions.py" is not a directory')
        ]

        for test in tests:
            result = get_files_info(test.working_directory, test.directory) 

            if test.isExpectErr:
                self.assertEqual(
                    result, test.expectedErrMsg
                )
            else:
                self.assertEqual(
                    "is_dir" in result, True
                )
    def test_get_file_content(self):
        class Test():
            def __init__(self,
                         working_directory,
                         file_path,
                         isExpectErr,
                         expectedErrMsg):
                self.working_directory = working_directory
                self.file_path = file_path
                self.isExpectErr = isExpectErr
                self.expectedErrMsg = expectedErrMsg

        tests = [
            Test(".", "../", True, 
                    f'Error: Cannot list "../" as it is outside the permitted working directory'),
            Test("../", "functions", True,
                              f'Error: File not found or is not a regular file: "functions"'),
            Test(".", "functions.py", False ,
                              f'Error: File not found or is not a regular file: "functions"')
        ]

        for test in tests:
            result = get_file_content(test.working_directory
                                      ,test.file_path)
            if test.isExpectErr:
                self.assertEqual(test.expectedErrMsg, result) 
            else:
                self.assertLessEqual(len(result), agent_config.max_chars)
            
if __name__ == "__main__":
    unittest.main()