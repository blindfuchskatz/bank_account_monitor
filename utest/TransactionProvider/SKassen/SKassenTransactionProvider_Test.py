import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.File.PdfReaderException import PdfReaderException
from src.TransactionProvider.SKasse.SKassenTransactionProvider import INVALID_INPUT_PATH, SKassenTransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from utest.TestHelper import CustomAssert
from src.TransactionProvider.TransactionConverterException import TransactionConverterException
from src.TransactionProvider.Transaction import Transaction

transactionGutschrift = """ some text
some text
21.08.2023 Gutschrift
a              100.000,09
some text
22.08.2023 Entgeltabrechnung
b              -6,90
some text"""

ta = Transaction("21.08.2023", "Gutschrift", "a", 10000009)
tb = Transaction("22.08.2023", "Entgeltabrechnung", "b", -690)

SOME_PATH = "/path/to/sort_rules"


class ASKassenTransactionProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.file_checker = FileChecker()

        self.read_file_content = PdfPageReader.read_file_content
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderException)

    def tearDown(self):
        PdfPageReader.read_file_content = self.read_file_content

    def testReturnEmptyTransactionList(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        PdfPageReader.read_file_content = MagicMock(
            return_value="no transaction")

        p = SKassenTransactionProvider(self.file_checker, SOME_PATH)
        t_list = p.get_transactions()
        self.assertListEqual(t_list, [])

    def testParseTransaction(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        PdfPageReader.read_file_content = MagicMock(
            return_value=transactionGutschrift)

        p = SKassenTransactionProvider(self.file_checker, SOME_PATH)
        t_list = p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])

    def testPassPdfPathToPdfReader(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        PdfPageReader.read_file_content = MagicMock(
            return_value=transactionGutschrift)

        p = SKassenTransactionProvider(self.file_checker, SOME_PATH)
        p.get_transactions()
        PdfPageReader.read_file_content.assert_called_once_with(SOME_PATH)

    def testForwardPdfReaderException(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        PdfPageReader.read_file_content = MagicMock(
            side_effect=PdfReaderException("some error"))

        p = SKassenTransactionProvider(self.file_checker, SOME_PATH)
        self.ca.assertRaisesWithMessage(
            "Transaction provider error|what:<some error>", p.get_transactions)

    def testForwardTransactionConverterException(self):
        self.file_checker.file_exists = MagicMock(return_value=True)
        PdfPageReader.read_file_content = MagicMock(
            side_effect=TransactionConverterException("some error"))

        p = SKassenTransactionProvider(self.file_checker, SOME_PATH)
        self.ca.assertRaisesWithMessage(
            "Transaction provider error|what:<some error>", p.get_transactions)

    def testRaiseExceptionWhenInputPathIsInvalid(self):
        self.file_checker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format(SOME_PATH), SKassenTransactionProvider, self.file_checker, SOME_PATH)
