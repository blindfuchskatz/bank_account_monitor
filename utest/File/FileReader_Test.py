import unittest
from unittest.mock import MagicMock
from src.File.FileReader import FileReader

NOT_RELEVANT = 'not relevant'


class AFileReader(unittest.TestCase):
    def setUp(self):
        self.read_file_content = FileReader.read_file_content

    def tearDown(self):
        FileReader.read_file_content = self.read_file_content

    def testIgnoreEmptyLines(self):
        FileReader.read_file_content = MagicMock(
            return_value="abc\n\nd\nee\r\nfffff\n\n")
        self.assertEqual(FileReader.get_lines(NOT_RELEVANT),
                         ['abc', 'd', 'ee', 'fffff'])

    def testStripLeadingAndTrailingWhiteSpaces(self):
        FileReader.read_file_content = MagicMock(
            return_value="     abc \n\nd    \nee \r\nfffff\n\n")
        self.assertEqual(FileReader.get_lines(NOT_RELEVANT),
                         ['abc', 'd', 'ee', 'fffff'])

    def testReturnEmptyLineList(self):
        FileReader.read_file_content = MagicMock(return_value="")
        self.assertEqual(FileReader.get_lines(NOT_RELEVANT), [])
