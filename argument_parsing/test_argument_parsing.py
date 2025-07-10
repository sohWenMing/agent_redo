import unittest
from argument_parsing import get_argument

class TestGetArgument(unittest.TestCase):
    def test_should_pass(self):
        self.assertEqual(get_argument([
            "main.py", "this is the prompt"
        ]), "this is the prompt")
    def test_should_fail(self):
        with self.assertRaises(ValueError):
            get_argument(["main.py"])

if __name__ == '__main__':
    unittest.main()