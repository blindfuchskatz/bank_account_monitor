from src.File.DirReader import DirReader
from src.TransactionProvider.Factory import Factory
from src.TransactionProvider.Transaction import TransactionList
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH, TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.TransactionProviderFactoryException import TransactionProviderFactoryException


class MultiTransactionProvider(TransactionProvider):
    def __init__(self, path: str, tp_factory: Factory) -> None:
        self.dir = path
        self.tp_factory = tp_factory

    def get_transactions(self) -> TransactionList:
        if not DirReader.is_dir(self.dir):
            raise TransactionProviderException(
                INVALID_INPUT_PATH.format("Multi", "dir does not exist"))

        file_list = DirReader.get_files_in_dir(self.dir)
        t_list = []

        for file in file_list:
            try:
                p = self.tp_factory.get_transaction_provider(file)
                t_list += p.get_transactions()

            except TransactionProviderFactoryException:
                continue

        return t_list

    def is_needed(self) -> bool:
        return DirReader.is_dir(self.dir)
