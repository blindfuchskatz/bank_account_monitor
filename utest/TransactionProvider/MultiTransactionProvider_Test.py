
import unittest
from unittest.mock import MagicMock
from src.File.DirReader import DirReader
from src.File.FileChecker import FileChecker
from src.TransactionProvider.MultiTransactionProvider import MultiTransactionProvider
from src.TransactionProvider.SKasse.SKassenTransactionProvider import SKassenTransactionProvider
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.VrBank.VrBankTransactionProvider import VrBankTransactionProvider
from utest.TestHelper import CustomAssert


ta = Transaction("21.08.2023", "Gutschrift", "a", 10000009)
tb = Transaction("22.08.2023", "Entgeltabrechnung", "b", -690)
tc = Transaction("23.08.2023", "Debit", "b", -990)

SOME_DIR = "/some/dir"


class AMultiTransactionProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.get_files_in_dir = DirReader.get_files_in_dir
        self.file_checker = FileChecker()
        self.file_checker.file_exists = MagicMock(return_value=True)
        self.file_checker.is_dir = MagicMock(return_value=True)

        self.skassen_is_account_statement = SKassenTransactionProvider.is_account_statement
        self.vrbank_is_account_statement = VrBankTransactionProvider.is_account_statement
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=True)
        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=True)

        self.skassen_gt = SKassenTransactionProvider.get_transactions
        self.vrbank_gt = VrBankTransactionProvider.get_transactions

        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionProviderException)

    def tearDown(self) -> None:
        DirReader.get_files_in_dir = self.get_files_in_dir
        SKassenTransactionProvider.is_account_statement = self.skassen_is_account_statement
        VrBankTransactionProvider.is_account_statement = self.vrbank_is_account_statement
        SKassenTransactionProvider.get_transactions = self.skassen_gt
        VrBankTransactionProvider.get_transactions = self.vrbank_gt

    def testReturnEmptyListWhenDirIsEmpty(self):
        DirReader.get_files_in_dir = MagicMock(return_value=[])
        p = MultiTransactionProvider(self.file_checker, SOME_DIR)
        t_list = p.get_transactions()
        self.assertListEqual(t_list, [])
        DirReader.get_files_in_dir.assert_called_once_with(SOME_DIR)

    def testReturnSkassenTransactions(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a"])
        SKassenTransactionProvider.get_transactions = MagicMock(return_value=[
                                                                ta, tb])
        p = MultiTransactionProvider(self.file_checker, SOME_DIR)
        t_list = p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])

    def testReturnVrBankTransactions(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a"])
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)
        VrBankTransactionProvider.get_transactions = MagicMock(return_value=[
            ta, tb])
        p = MultiTransactionProvider(self.file_checker, SOME_DIR)
        t_list = p.get_transactions()

        self.assertListEqual(t_list, [ta, tb])

    def testReturnSKassenAndVrBankTransactions(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a", "/b", "/c"])
        SKassenTransactionProvider.is_account_statement = MagicMock()
        SKassenTransactionProvider.is_account_statement.side_effect = [
            True, False, True]

        SKassenTransactionProvider.get_transactions = MagicMock()
        SKassenTransactionProvider.get_transactions.side_effect = [[ta], [tc]]
        VrBankTransactionProvider.get_transactions = MagicMock(return_value=[
            tb])
        p = MultiTransactionProvider(self.file_checker, SOME_DIR)
        t_list = p.get_transactions()

        self.assertListEqual(t_list, [ta, tb, tc])

    def testIgnoreNotAccountStatementFiles(self):
        DirReader.get_files_in_dir = MagicMock(return_value=["/a", "/b", "/c"])
        SKassenTransactionProvider.is_account_statement = MagicMock(
            return_value=False)

        VrBankTransactionProvider.is_account_statement = MagicMock(
            return_value=False)

        p = MultiTransactionProvider(self.file_checker, SOME_DIR)
        t_list = p.get_transactions()

        self.assertListEqual(t_list, [])

    def testRaiseExceptionWhenDirNotExists(self):
        DirReader.get_files_in_dir = MagicMock()
        self.file_checker.is_dir = MagicMock(return_value=False)

        p = MultiTransactionProvider(self.file_checker, SOME_DIR)
        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format("Multi", "dir does not exist"), p.get_transactions)
