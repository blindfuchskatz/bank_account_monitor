import re
from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.TransactionProvider.SKasse.SKassenTransactionConverter import SKassenTransactionConverter
from src.TransactionProvider.SKasse.SKassenTransactionExtractor import SKassenTransactionExtractor
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException

PROVIDER_EXCEPTION = "SKassen transaction provider error|what:<{}>"
IS_NOT_ACCOUNT_STATEMENT = "no skassen account statement"


class SKassenTransactionProvider(TransactionProvider):
    def __init__(self, file_checker, path):
        super().__init__(file_checker, path, "SKassen")
        if not self.is_account_statement():
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(IS_NOT_ACCOUNT_STATEMENT))

    def get_transactions(self):
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
