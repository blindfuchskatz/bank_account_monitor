from src.File.FileChecker import FileChecker
from src.File.PdfPageReader import PdfPageReader
from src.TransactionProvider.SKasse.SKassenTransactionConverter import SKassenTransactionConverter
from src.TransactionProvider.SKasse.SKassenTransactionExtractor import SKassenTransactionExtractor
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException

PROVIDER_EXCEPTION = "SKassen transaction provider error|what:<{}>"


class SKassenTransactionProvider(TransactionProvider):
    def __init__(self, file_checker, path):
        super().__init__(file_checker, path, "SKassen")

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
