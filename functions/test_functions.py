import unittest
from functions import get_files_info

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
                print(result)
                self.assertEqual(
                    "is_dir" in result, True
                )

if __name__ == "__main__":
    unittest.main()