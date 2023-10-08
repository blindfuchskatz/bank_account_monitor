import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.TransactionProvider.MultiTransactionProvider import MultiTransactionProvider

from src.TransactionProvider.SKasse.SKassenTransactionProvider import SKassenTransactionProvider
from src.TransactionProvider.TransactionProviderFactory import FILE_NOT_EXIST, NOT_A_ACCOUNT_STATEMENT, TransactionProviderFactory
from src.TransactionProvider.TransactionProviderFactoryException import TransactionProviderFactoryException
from src.TransactionProvider.VrBank.VrBankTransactionProvider import VrBankTransactionProvider
from utest.TestHelper import CustomAssert

SOME_PATH = "some path"


class ATransactionProviderFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderFactoryException)

        self.factory = TransactionProviderFactory()

        self.multi_is_needed = MultiTransactionProvider.is_needed
        self.skassen_is_account_statement = SKassenTransactionProvider.is_account_statement
        self.vrbank_is_account_statement = VrBankTransactionProvider.is_account_statement
        self.file_exists = TransactionProviderFactory.file_exists
        TransactionProviderFactory.file_exists = MagicMock(return_value=True)

    def tearDown(self) -> None:
        MultiTransactionProvider.is_needed = self.multi_is_needed
        SKassenTransactionProvider.is_account_statement = self.skassen_is_account_statement
        VrBankTransactionProvider.is_account_statement = self.vrbank_is_account_statement
        TransactionProviderFactory.file_exists = self.file_exists

    def testReturnSKassenTransactionProvider(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=False)
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=True)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=False)

        p = self.factory.get_transaction_provider(SOME_PATH)

        self.assertEqual(type(p), SKassenTransactionProvider)

    def testPathIsPassedToSKassenTransactionProvider(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=False)
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=True)

        original_constructor = SKassenTransactionProvider.__init__
        SKassenTransactionProvider.__init__ = MagicMock(return_value=None)

        self.factory.get_transaction_provider(SOME_PATH)

        SKassenTransactionProvider.__init__.assert_called_with(SOME_PATH)
        SKassenTransactionProvider.__init__ = original_constructor

    def testReturnVrBankTransactionProvider(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=False)
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=True)

        p = self.factory.get_transaction_provider(SOME_PATH)

        self.assertEqual(type(p), VrBankTransactionProvider)

    def testPathIsPassedToVrBankTransactionProvider(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=False)
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=True)

        original_constructor = VrBankTransactionProvider.__init__
        VrBankTransactionProvider.__init__ = MagicMock(return_value=None)

        self.factory.get_transaction_provider(SOME_PATH)

        VrBankTransactionProvider.__init__.assert_called_with(SOME_PATH)
        VrBankTransactionProvider.__init__ = original_constructor

    def testReturnMultiTransactionProvider(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=True)

        p = self.factory.get_transaction_provider(SOME_PATH)

        self.assertEqual(type(p), MultiTransactionProvider)

    def testPathIsPassedToMultiTransactionProvider(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=True)

        original_constructor = MultiTransactionProvider.__init__
        MultiTransactionProvider.__init__ = MagicMock(return_value=None)

        self.factory.get_transaction_provider(SOME_PATH)

        MultiTransactionProvider.__init__.assert_called_with(
            SOME_PATH, self.factory)
        MultiTransactionProvider.__init__ = original_constructor

    def testCheckIfAFileExists(self):
        TransactionProviderFactory.file_exists = self.file_exists
        file_exists = FileChecker.file_exists
        FileChecker.file_exists = MagicMock(return_value=False)

        self.assertEqual(False, self.factory.file_exists("path"))

        FileChecker.file_exists = file_exists

    def testRaiseExceptionForAUnknownAccountStatement(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=False)
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=False)

        self.ca.assertRaisesWithMessage(
            NOT_A_ACCOUNT_STATEMENT.format(SOME_PATH), self.factory.get_transaction_provider, SOME_PATH)

    def testRaiseExceptionForNotExistingFile(self):
        MultiTransactionProvider.is_needed = MagicMock(return_value=False)
        TransactionProviderFactory.file_exists = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            FILE_NOT_EXIST.format(SOME_PATH), self.factory.get_transaction_provider, SOME_PATH)
