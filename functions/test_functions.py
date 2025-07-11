import unittest
from functions import (
    get_files_info, 
    get_file_content, 
    write_file, 
    run_python_file
)
import os

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
                self.assertLessEqual(len(result), 10000)
            
    def test_write_file(self):
        class Test():
            def __init__(self,
                         working_directory,
                         file_path, content,
                         isExpectErr,
                         expectedErrMsg):
                self.working_directory = working_directory
                self.file_path = file_path
                self.content = content
                self.isExpectErr = isExpectErr
                self.expectedErrMsg = expectedErrMsg

        tests = [
            Test(".", "test.txt", "this is the test content", False, None),
            Test(".", "../test.txt", "this is the test content", True, 
                 f'Error: Cannot write to "../test.txt" as it is outside the permitted working directory')
        ]

        for test in tests:
            result = write_file(test.working_directory, test.file_path, test.content)
            print("result: ", result)
            if not test.isExpectErr:
                full_path = os.path.join(os.path.abspath(test.working_directory), test.file_path)
                with open(full_path, "r") as f:
                    data = f.read()
                    self.assertEqual(test.content, str(data))
                os.remove(full_path) 
            else:
                self.assertEqual(test.expectedErrMsg, result)

    def test_run_python_file(self):
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
            Test(".", "../calculator/main.py", True,
                f'Error: Cannot execute "../calculator/main.py" as it is outside the permitted working directory'),
            Test(".", "shouldfail.py", True, f'Error: File "shouldfail.py" not found.'),
            Test("../", "calculator/package/lorem.txt", True, f'Error: file "calculator/package/lorem.txt" not found.')
        ]

        for test in tests:
            result = run_python_file(test.working_directory, test.file_path)
            if test.isExpectErr:
                self.assertEqual(test.expectedErrMsg, result)

if __name__ == "__main__":
    unittest.main()