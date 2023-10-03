import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker

from src.TransactionProvider.SKasse.SKassenTransactionProvider import SKassenTransactionProvider
from src.TransactionProvider.TransactionProviderFactory import FILE_NOT_EXIST, NOT_A_ACCOUNT_STATEMENT, TransactionProviderFactory
from src.TransactionProvider.TransactionProviderFactoryException import TransactionProviderFactoryException
from src.TransactionProvider.VrBank.VrBankTransactionProvider import VrBankTransactionProvider
from utest.TestHelper import CustomAssert

SOME_PATH = "some path"


class ATransactionProviderFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.file_exists = FileChecker.file_exists
        FileChecker.file_exists = MagicMock(return_value=True)

        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderFactoryException)

        self.factory = TransactionProviderFactory()

        self.skassen_is_account_statement = SKassenTransactionProvider.is_account_statement
        self.vrbank_is_account_statement = VrBankTransactionProvider.is_account_statement

    def tearDown(self) -> None:
        FileChecker.file_exists = self.file_exists
        SKassenTransactionProvider.is_account_statement = self.skassen_is_account_statement
        VrBankTransactionProvider.is_account_statement = self.vrbank_is_account_statement

    def testReturnSKassenTransactionProvider(self):
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=True)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=False)

        p = self.factory.get_transaction_provider(SOME_PATH)

        self.assertEqual(type(p), SKassenTransactionProvider)

    def testPathIsPassedToSKassenTransactionProvider(self):
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=True)
        self.factory.get_transaction_provider(SOME_PATH)

        FileChecker.file_exists.assert_called_with(SOME_PATH)

    def testReturnVrBankTransactionProvider(self):
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=True)

        p = self.factory.get_transaction_provider(SOME_PATH)

        self.assertEqual(type(p), VrBankTransactionProvider)

    def testPathIsPassedToVrBankTransactionProvider(self):
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=True)

        self.factory.get_transaction_provider(SOME_PATH)

        FileChecker.file_exists.assert_called_with(SOME_PATH)

    def testRaiseExceptionForAUnknownAccountStatement(self):
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=False)

        self.ca.assertRaisesWithMessage(
            NOT_A_ACCOUNT_STATEMENT.format(SOME_PATH), self.factory.get_transaction_provider, SOME_PATH)

    def testRaiseExceptionForNotExistingFile(self):
        FileChecker.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            FILE_NOT_EXIST.format(SOME_PATH), self.factory.get_transaction_provider, SOME_PATH)

        FileChecker.file_exists.assert_called_once_with(SOME_PATH)
