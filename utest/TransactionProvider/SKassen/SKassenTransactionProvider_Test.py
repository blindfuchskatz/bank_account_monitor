import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.File.PdfReaderException import PdfReaderException
from src.TransactionProvider.SKasse.SKassenTransactionExtractor import SKassenTransactionExtractor
from src.TransactionProvider.SKasse.SKassenTransactionProvider import IS_NOT_ACCOUNT_STATEMENT, PROVIDER_EXCEPTION, SKassenTransactionProvider
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from utest.TestHelper import CustomAssert
from src.TransactionProvider.TransactionConverterException import TransactionConverterException
from src.TransactionProvider.Transaction import Transaction

transactionGutschrift = """ Skassen some text
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
        self.file_exists = FileChecker.file_exists
        FileChecker.file_exists = MagicMock(return_value=True)

        self.read_file_content = PdfPageReader.read_file_content
        self.is_pdf = PdfPageReader.is_pdf
        PdfPageReader.is_pdf = MagicMock(return_value=True)

        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderException)

        self.p = SKassenTransactionProvider(SOME_PATH)

    def tearDown(self):
        PdfPageReader.read_file_content = self.read_file_content
        PdfPageReader.is_pdf = self.is_pdf
        FileChecker.file_exists = self.file_exists

    def testReturnEmptyTransactionList(self):
        PdfPageReader.read_file_content = MagicMock(
            return_value="Skassen:no transaction")

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
        PdfPageReader.read_file_content.assert_called_with(SOME_PATH)

    def testRaiseExceptionIfNoPdfFile(self):
        PdfPageReader.is_pdf = MagicMock(
            return_value=False)

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(IS_NOT_ACCOUNT_STATEMENT), self.p.get_transactions)

    def testRaiseExceptionIfNoSKassenPattern(self):
        PdfPageReader.is_pdf = MagicMock(
            return_value=True)

        PdfPageReader.read_file_content = MagicMock(
            return_value="Vr bank")

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(IS_NOT_ACCOUNT_STATEMENT), self.p.get_transactions)

    def testForwardPdfReaderException(self):
        PdfPageReader.read_file_content = MagicMock(
            side_effect=PdfReaderException("e"))

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format("e"), self.p.get_transactions)

    def testForwardExtractorException(self):
        PdfPageReader.read_file_content = MagicMock(
            return_value="Skassen:no transaction")
        extract = SKassenTransactionExtractor.extract

        SKassenTransactionExtractor.extract = MagicMock(
            side_effect=Exception("error"))
        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format("error"), self.p.get_transactions)

        SKassenTransactionExtractor.extract = extract

    def testForwardTransactionConverterException(self):
        PdfPageReader.read_file_content = MagicMock(
            side_effect=TransactionConverterException(SOME_ERROR))

        self.ca.assertRaisesWithMessage(
            PROVIDER_EXCEPTION.format(SOME_ERROR), self.p.get_transactions)

    def testRaiseExceptionWhenInputPathIsInvalid(self):
        FileChecker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format("SKassen", SOME_PATH), self.p.get_transactions)
