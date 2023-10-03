
from abc import abstractmethod
from src.File.FileChecker import FileChecker

from src.TransactionProvider.TransactionProviderException import TransactionProviderException

INVALID_INPUT_PATH = "{} transaction provider error|invalid input path|path:<{}>"


class TransactionProvider:
    def __init__(self, file_checker: FileChecker, path: str, name: str) -> None:
        self._file_checker = file_checker
        self._path = path
        self._name = name

        if not self._file_checker.file_exists(self._path):
            raise TransactionProviderException(
                INVALID_INPUT_PATH.format(self._name, self._path))

    @abstractmethod
    def get_transactions(self):
        pass
