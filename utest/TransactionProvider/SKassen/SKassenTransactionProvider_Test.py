import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.File.PdfReaderException import PdfReaderException
from src.TransactionProvider.SKasse.SKassenTransactionProvider import PROVIDER_EXCEPTION, SKassenTransactionProvider
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH
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
SOME_ERROR = "some error"


class ASKassenTransactionProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.file_checker = FileChecker()
        self.file_checker.file_exists = MagicMock(return_value=True)
        self.p = SKassenTransactionProvider(self.file_checker, SOME_PATH)

        self.read_file_content = PdfPageReader.read_file_content
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderException)

    def tearDown(self):
        PdfPageReader.read_file_content = self.read_file_content

    def testReturnEmptyTransactionList(self):
        PdfPageReader.read_file_content = MagicMock(
            return_value="no transaction")

        t_list = self.p.get_transactions()
        self.assertListEqual(t_list, [])

    def testParseTransaction(self):
        PdfPageReader.read_file_content = MagicMock(
            return_value=transactionGutschrift)

        t_list = self.p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])

    def testPassPdfPathToPdfReader(self):
        PdfPageReader.read_file_content = MagicMock(
            return_value=transactionGutschrift)

        self.p.get_transactions()
        PdfPageReader.read_file_content.assert_called_once_with(SOME_PATH)

    def testForwardPdfReaderException(self):
        PdfPageReader.read_file_content = MagicMock(
            side_effect=PdfReaderException(SOME_ERROR))

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(SOME_ERROR), self.p.get_transactions)

    def testForwardTransactionConverterException(self):
        PdfPageReader.read_file_content = MagicMock(
            side_effect=TransactionConverterException(SOME_ERROR))

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(SOME_ERROR), self.p.get_transactions)

    def testRaiseExceptionWhenInputPathIsInvalid(self):
        self.file_checker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format("SKassen", SOME_PATH), SKassenTransactionProvider, self.file_checker, SOME_PATH)
