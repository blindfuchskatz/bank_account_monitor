import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.File.FileReader import FileReader
from src.File.FileReaderException import FileReaderException
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.VrBank.VrBankTransactionConverter import FORMAT_ERROR_TO_FEW_LINES, NUMBER_CSV_ENTRIES
from src.TransactionProvider.VrBank.VrBankTransactionProvider import INVALID_INPUT_PATH, PROVIDER_EXCEPTION, VrBankTransactionProvider

from utest.TestHelper import CustomAssert

SOME_PATH = "/some/path"
SOME_ERROR = "some error"


class AVrBankTransactionProvider(unittest.TestCase):
    def setUp(self):
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderException)
        self.get_lines = FileReader.get_lines
        self.file_checker = FileChecker()
        self.file_checker.file_exists = MagicMock(return_value=True)
        self.p = VrBankTransactionProvider(self.file_checker, SOME_PATH)

    def tearDown(self):
        FileReader.get_lines = self.get_lines

    def testReturnEmptyTransactionList(self):
        FileReader.get_lines = MagicMock(return_value=[])

        t_list = self.p.get_transactions()
        self.assertListEqual(t_list, [])

    def testPassPathArgumentToFileReader(self):
        FileReader.get_lines = MagicMock(return_value=[])
        self.p.get_transactions()

        FileReader.get_lines.assert_called_once_with(SOME_PATH)

    def testParseTransaction(self):
        csv_head_line = "a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r;s"
        line1 = "a;b;c;d;30.09.2023;f;g;h;i;debit;desc1;-76,76;m;n;o;p;q;r;s"
        line2 = "a;b;c;d;30.09.2023;f;g;h;i;gift;desc2;10.000,23;m;n;o;p;q;r;s"
        ta = Transaction("30.09.2023", "debit", "desc1", -7676)
        tb = Transaction("30.09.2023", "gift", "desc2", 1000023)
        csv_lines = [csv_head_line, line1, line2]
        FileReader.get_lines = MagicMock(return_value=csv_lines)

        t_list = self.p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])

    def testForwardFileReaderException(self):
        FileReader.get_lines = MagicMock(
            side_effect=FileReaderException(SOME_ERROR))

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(SOME_ERROR), self.p.get_transactions)

    def testForwardTransactionConverterException(self):
        csv_head_line = "hello"
        line1 = "servus"
        FileReader.get_lines = MagicMock(return_value=[csv_head_line, line1])

        e = PROVIDER_EXCEPTION.format(
            FORMAT_ERROR_TO_FEW_LINES.format(NUMBER_CSV_ENTRIES, 1))
        self.ca.assertRaisesWithMessage(e, self.p.get_transactions)

    def testRaiseExceptionWhenInputPathIsInvalid(self):
        self.file_checker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format(SOME_PATH), VrBankTransactionProvider, self.file_checker, SOME_PATH)
