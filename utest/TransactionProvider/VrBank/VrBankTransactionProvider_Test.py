import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.File.FileReader import FileReader
from src.File.FileReaderException import FileReaderException
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.VrBank.VrBankTransactionConverter import FORMAT_ERROR_TO_FEW_LINES, NUMBER_CSV_ENTRIES
from src.TransactionProvider.VrBank.VrBankTransactionProvider import HEAD_LINE, IS_NOT_ACCOUNT_STATEMENT, PROVIDER_EXCEPTION, VrBankTransactionProvider

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

    def tearDown(self):
        FileReader.get_lines = self.get_lines

    def testReturnEmptyTransactionList(self):
        FileReader.get_lines = MagicMock(return_value=[HEAD_LINE])

        p = VrBankTransactionProvider(self.file_checker, SOME_PATH)

        t_list = p.get_transactions()
        self.assertListEqual(t_list, [])

    def testPassPathArgumentToFileReader(self):
        FileReader.get_lines = MagicMock(return_value=[HEAD_LINE])
        p = VrBankTransactionProvider(self.file_checker, SOME_PATH)

        p.get_transactions()

        FileReader.get_lines.assert_called_with(SOME_PATH)

    def testParseTransaction(self):
        line1 = "a;b;c;d;30.09.2023;f;g;h;i;debit;desc1;-76,76;m;n;o;p;q;r;s"
        line2 = "a;b;c;d;30.09.2023;f;g;h;i;gift;desc2;10.000,23;m;n;o;p;q;r;s"
        ta = Transaction("30.09.2023", "debit", "desc1", -7676)
        tb = Transaction("30.09.2023", "gift", "desc2", 1000023)
        csv_lines = [HEAD_LINE, line1, line2]
        FileReader.get_lines = MagicMock(return_value=csv_lines)
        p = VrBankTransactionProvider(self.file_checker, SOME_PATH)

        t_list = p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])

    def testForwardFileReaderException(self):
        FileReader.get_lines = MagicMock(
            side_effect=FileReaderException(SOME_ERROR))

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(SOME_ERROR), VrBankTransactionProvider, self.file_checker, SOME_PATH)

    def testForwardTransactionConverterException(self):
        line1 = "servus"
        FileReader.get_lines = MagicMock(return_value=[HEAD_LINE, line1])

        p = VrBankTransactionProvider(self.file_checker, SOME_PATH)

        e = PROVIDER_EXCEPTION.format(
            FORMAT_ERROR_TO_FEW_LINES.format(NUMBER_CSV_ENTRIES, 1))
        self.ca.assertRaisesWithMessage(e, p.get_transactions)

    def testRaiseExceptionWhenNoLines(self):
        FileReader.get_lines = MagicMock(return_value=[])

        e = PROVIDER_EXCEPTION.format(IS_NOT_ACCOUNT_STATEMENT)
        self.ca.assertRaisesWithMessage(
            e, VrBankTransactionProvider, self.file_checker, SOME_PATH)

    def tesRaiseExceptionWhenHeadlineMissing(self):
        FileReader.get_lines = MagicMock(return_value=[])
        self.assertEqual(self.p.is_account_statement(SOME_PATH), False)

        FileReader.get_lines = MagicMock(return_value=["hello"])
        self.assertEqual(self.p.is_account_statement(SOME_PATH), False)

    def testRaiseExceptionWhenInputPathIsInvalid(self):
        self.file_checker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format("VR bank", SOME_PATH), VrBankTransactionProvider, self.file_checker, SOME_PATH)
