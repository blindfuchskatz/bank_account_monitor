from typing import List
from src.File.FileChecker import FileChecker
from src.File.FileReader import FileReader
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.VrBank.VrBankTransactionConverter import VrBankTransactionConverter


PROVIDER_EXCEPTION = "VR bank transaction provider error|what:<{}>"
INVALID_INPUT_PATH = "VR bank transaction provider error|invalid input path|path:<{}>"


class VrBankTransactionProvider(TransactionProvider):
    def __init__(self, file_checker: FileChecker, path: str) -> None:
        super().__init__()
        self.__path = path
        self.__file_checker = file_checker

        if not self.__file_checker.file_exists(self.__path):
            raise TransactionProviderException(
                INVALID_INPUT_PATH.format(self.__path))

    def get_transactions(self) -> List[Transaction]:
        try:
            csv_line_list = FileReader.get_lines(self.__path)
            t_list = []
            c = VrBankTransactionConverter()

            for csv_line in csv_line_list[1:]:
                t_list.append(c.convert(csv_line))

            return t_list
        except Exception as e:
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(str(e)))
