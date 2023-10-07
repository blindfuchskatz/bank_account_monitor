import unittest
from unittest.mock import MagicMock
from src.File.DirReader import DirReader
from src.File.FileChecker import FileChecker
from src.TransactionProvider.MultiTransactionProvider import MultiTransactionProvider
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH, TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.TransactionProviderFactory import TransactionProviderFactory
from src.TransactionProvider.TransactionProviderFactoryException import TransactionProviderFactoryException
from utest.TestHelper import CustomAssert


ta = Transaction("21.08.2023", "Gutschrift", "a", 10000009)
tb = Transaction("22.08.2023", "Entgeltabrechnung", "b", -690)

SOME_DIR = "/some/dir"


class TPStub(TransactionProvider):
    def get_transactions(self):
        return [ta, tb]


tpStub = TPStub()


class AMultiTransactionProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.tpf = TransactionProviderFactory()
        self.get_files_in_dir = DirReader.get_files_in_dir
        self.file_checker = FileChecker()
        self.file_checker.is_dir = MagicMock(side_effect=[True, False])

        self.p = MultiTransactionProvider(
            self.file_checker, SOME_DIR, self.tpf)

        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderException)

    def tearDown(self) -> None:
        DirReader.get_files_in_dir = self.get_files_in_dir

    def testReturnEmptyListWhenDirIsEmpty(self):
        DirReader.get_files_in_dir = MagicMock(return_value=[])
        self.file_checker.is_dir = MagicMock(return_value=True)

        t_list = self.p.get_transactions()

        self.assertListEqual(t_list, [])
        DirReader.get_files_in_dir.assert_called_once_with(SOME_DIR)

    def testReturnTransactionsOfOneAccountStatement(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a"])
        self.tpf.get_transaction_provider = MagicMock(return_value=tpStub)

        t_list = self.p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])
        self.tpf.get_transaction_provider.assert_called_once_with("/a")

    def testConcatenateTransactionsOfMultipleAccountStatements(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a", "/b", "/c"])
        self.tpf.get_transaction_provider = MagicMock(return_value=tpStub)

        t_list = self.p.get_transactions()

        self.assertListEqual(t_list, [ta, tb, ta, tb, ta, tb])

    def testIgnoreNotAccountStatementFiles(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a", "/b", "/c"])

        self.tpf.get_transaction_provider = MagicMock(
            side_effect=TransactionProviderFactoryException)

        t_list = self.p.get_transactions()

        self.assertListEqual(t_list, [])

    def testRaiseExceptionWhenDirNotExists(self):
        DirReader.get_files_in_dir = MagicMock()
        self.file_checker.is_dir = MagicMock(return_value=False)

        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format("Multi", "dir does not exist"), self.p.get_transactions)
