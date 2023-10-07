

from src.File.DirReader import DirReader
from src.File.FileChecker import FileChecker
from src.TransactionProvider.SKasse.SKassenTransactionProvider import SKassenTransactionProvider
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH, TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.VrBank.VrBankTransactionProvider import VrBankTransactionProvider


class MultiTransactionProvider(TransactionProvider):
    def __init__(self, file_checker: FileChecker, path: str) -> None:
        self.file_checker = file_checker
        self.dir = path

    def get_transactions(self):
        if not self.file_checker.is_dir(self.dir):
            raise TransactionProviderException(
                INVALID_INPUT_PATH.format("Multi", "dir does not exist"))

        file_list = DirReader.get_files_in_dir(self.dir)
        t_list = []

        # todo PWA: refactor
        for file in file_list:
            try:
                p = SKassenTransactionProvider(self.file_checker, file)
                t_list += p.get_transactions()

                continue
            except TransactionProviderException:
                pass
            try:
                p = VrBankTransactionProvider(self.file_checker, file)
                t_list += p.get_transactions()

                continue
            except TransactionProviderException:
                pass

        return t_list
