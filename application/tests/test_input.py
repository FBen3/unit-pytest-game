import unittest
from unittest.mock import patch

from application.process_input import load_input


class TestInput(unittest.TestCase):


    def test_only_one_argument_is_specified(self):
        with self.assertRaises(IndexError) as context:
            load_input(['input_1.txt','input_2.txt'])

        self.assertTrue("Please specify 1 argument" in str(context.exception))

    @patch("os.path.isfile")
    def test_user_argument_is_a_text_file(self, mock_isfile):
        mock_isfile.return_value = True
        with self.assertRaises(TypeError) as context:
            load_input(['not_text_file.json'])

        self.assertTrue("Input must be a text file" in str(context.exception))

    @patch("os.path.isfile")
    def test_input_file_not_found(self, mock_isfile):
        mock_isfile.return_value = False
        with self.assertRaises(FileNotFoundError) as context:
            load_input(['non_existent_file.txt'])

        self.assertTrue("Could not find file" in str(context.exception))

    def test_no_argument_specified(self):
        with self.assertRaises(IndexError) as context:
            load_input([])

        self.assertTrue("Please specify 1 argument" in str(context.exception))

    # def test_input_file_is_pipe_delimited(self):
    #     return





if __name__ == '__main__':
    unittest.main()

# if I want to test that a function raises an error
#     with self.assertRaises(ValueError):
#         print_stats()


