import re
from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.TransactionProvider.SKasse.SKassenTransactionConverter import SKassenTransactionConverter
from src.TransactionProvider.SKasse.SKassenTransactionExtractor import SKassenTransactionExtractor
from src.TransactionProvider.Transaction import TransactionList
from src.TransactionProvider.TransactionProvider import INVALID_INPUT_PATH, TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException

PROVIDER_EXCEPTION = "SKassen transaction provider error|what:<{}>"
IS_NOT_ACCOUNT_STATEMENT = "no skassen account statement"


class SKassenTransactionProvider(TransactionProvider):
    def __init__(self, path: str):
        self._path = path

    def get_transactions(self) -> TransactionList:
        if not FileChecker.file_exists(self._path):
            raise TransactionProviderException(
                INVALID_INPUT_PATH.format("SKassen", self._path))

        if not self.is_account_statement():
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(IS_NOT_ACCOUNT_STATEMENT))

        try:
            r = PdfPageReader()
            e = SKassenTransactionExtractor()
            c = SKassenTransactionConverter()

            text = r.read_file_content(self._path)

            t_list = []

            raw_trans_list = e.extract(text)

            for raw_trans in raw_trans_list:
                t_list.append(c.convert(raw_trans))

            return t_list
        except Exception as e:
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(str(e)))

    def is_account_statement(self) -> bool:
        try:
            r = PdfPageReader()
            if not r.is_pdf(self._path):
                return False

            regex_pattern = r"S.*?kasse"
            text = r.read_file_content(self._path)

            match = re.findall(regex_pattern, text)
            if match:
                return True

            return False
        except Exception as e:
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(str(e)))
