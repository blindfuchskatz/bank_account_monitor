
from abc import abstractmethod
from src.File.FileChecker import FileChecker

from src.TransactionProvider.TransactionProviderException import TransactionProviderException

INVALID_INPUT_PATH = "{} transaction provider error|invalid input path|path:<{}>"


class TransactionProvider:
    @abstractmethod
    def get_transactions(self):
        pass
