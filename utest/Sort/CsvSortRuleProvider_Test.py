import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker

from src.Sort.CsvSortRuleProvider import INVALID_INPUT_PATH, MAX_NUMBER_SORT_RULES, TOO_MUCH_SORT_RULES, CsvSortRuleProvider
from src.Sort.CsvSortRuleProvider import INVALID_LINE
from src.Sort.CsvSortRuleProvider import TOO_MUCH_SEARCH_PATTERN
from src.File.FileReader import FileReader
from src.File.FileReaderException import FileReaderException

from src.Sort.SortRule import SortRule
from src.Sort.SortRuleProviderException import SortRuleProviderException
from utest.TestHelper import CustomAssert

SOME_PATH = "/path/to/sort_rules"


class ACsvSortRuleProvider(unittest.TestCase):

    def setUp(self) -> None:
        self.get_lines = FileReader.get_lines
        self.file_checker = FileChecker()
        self.ca = CustomAssert()
        self.ca.setExceptionType(SortRuleProviderException)

    def tearDown(self):
        FileReader.get_lines = self.get_lines

    def testReturnEmptySortRuleList(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        FileReader.get_lines = MagicMock(return_value=[])

        r_list = p.get_sort_rules()

        self.assertListEqual(r_list, [])

    def testReturnOneSortRule(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line = "Insurance;HUK;\"Allianz; car\";12345; Degenia"
        r1 = SortRule(
            "Insurance", ["HUK", "Allianz; car", "12345", " Degenia"])
        FileReader.get_lines = MagicMock(return_value=[csv_line])

        r_list = p.get_sort_rules()

        self.assertListEqual(r_list, [r1])

    def testReturnMultiSortRule(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line1 = "Insurance;HUK;Degenia"
        csv_line2 = "Car;Shell;Leasing;Gas;Tax"
        r1 = SortRule("Insurance", ["HUK", "Degenia"])
        r2 = SortRule("Car", ["Shell", "Leasing", "Gas", "Tax"])

        FileReader.get_lines = MagicMock(
            return_value=[csv_line1, csv_line2])

        r_list = p.get_sort_rules()

        self.assertListEqual(r_list, [r1, r2])

    def testPassPathToFileReader(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        FileReader.get_lines = MagicMock()

        p.get_sort_rules()

        FileReader.get_lines.assert_called_once_with(SOME_PATH)

    def testRaiseExceptionNoCsv(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line1 = "Insurance;HUK;Degenia"
        csv_line2 = "hallo"
        csv_line3 = "Car;Shell;Leasing;Gas;Tax"
        csv_lines = [csv_line1, csv_line2, csv_line3]

        FileReader.get_lines = MagicMock(return_value=csv_lines)

        e = INVALID_LINE.format(csv_line2)

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testRaiseExceptionNoCategory(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line = ";HUK;Degenia"
        FileReader.get_lines = MagicMock(return_value=[csv_line])

        e = INVALID_LINE.format(csv_line)

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testRaiseExceptionNoPattern(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line = "Car;"
        FileReader.get_lines = MagicMock(return_value=[csv_line])

        e = INVALID_LINE.format(csv_line)

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testRaiseExceptionMissingPattern(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line = "Car;;Leasing;Gas"
        FileReader.get_lines = MagicMock(return_value=[csv_line])

        e = INVALID_LINE.format(csv_line)

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testRaiseExceptionMoreThan100Pattern(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_line = "Car;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a;b;c;d;e;f;g;h;i;k;a"
        FileReader.get_lines = MagicMock(return_value=[csv_line])

        e = TOO_MUCH_SEARCH_PATTERN.format("Car", 101)

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testRaiseExceptionMoreThan100SortRules(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        csv_lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8,
                     9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        FileReader.get_lines = MagicMock(return_value=csv_lines)

        e = TOO_MUCH_SORT_RULES.format(MAX_NUMBER_SORT_RULES, 101)

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testForwardFileReaderExceptions(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        p = CsvSortRuleProvider(self.file_checker, SOME_PATH)

        e = "some error"

        FileReader.get_lines = MagicMock(side_effect=FileReaderException(e))

        self.ca.assertRaisesWithMessage(e, p.get_sort_rules)

    def testExceptionWhenInputPathIsInvalid(self):
        self.file_checker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format(SOME_PATH), CsvSortRuleProvider, self.file_checker, SOME_PATH)
