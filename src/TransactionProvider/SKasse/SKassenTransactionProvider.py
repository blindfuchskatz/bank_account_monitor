from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.TransactionProvider.SKasse.SKassenTransactionConverter import SKassenTransactionConverter
from src.TransactionProvider.SKasse.SKassenTransactionExtractor import SKassenTransactionExtractor
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException

INVALID_INPUT_PATH = "SKassen transaction provider error|invalid input path|path:<{}>"


class SKassenTransactionProvider(TransactionProvider):
    def __init__(self, file_checker, path):
        self.file_checker = file_checker
        self.__path = path

        if not self.file_checker.file_exists(self.__path):
            raise TransactionProviderException(
                INVALID_INPUT_PATH.format(self.__path))

    def get_transactions(self):
        try:
            r = PdfPageReader()
            e = SKassenTransactionExtractor()
            c = SKassenTransactionConverter()

            text = r.read_file_content(self.__path)
            t_list = []

            raw_trans_list = e.extract(text)

            for raw_trans in raw_trans_list:
                t_list.append(c.convert(raw_trans))

            return t_list
        except Exception as e:
            raise TransactionProviderException(
                "Transaction provider error|what:<{}>".format(str(e)))
