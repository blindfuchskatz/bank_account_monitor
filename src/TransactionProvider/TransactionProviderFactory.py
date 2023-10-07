from src.File.FileChecker import FileChecker
from src.TransactionProvider.MultiTransactionProvider import MultiTransactionProvider
from src.TransactionProvider.SKasse.SKassenTransactionProvider import SKassenTransactionProvider
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.TransactionProviderFactoryException import TransactionProviderFactoryException
from src.TransactionProvider.VrBank.VrBankTransactionProvider import VrBankTransactionProvider

NOT_A_ACCOUNT_STATEMENT = "Not supported bank account statement file|file:<{}>"
FILE_NOT_EXIST = "Account statement file does not exist:<{}>"


class TransactionProviderFactory:
    def get_transaction_provider(self, path: str) -> TransactionProvider:
        file_checker = FileChecker()

        if (file_checker.is_dir(path)):
            return MultiTransactionProvider(file_checker, path)

        if not file_checker.file_exists(path):
            raise TransactionProviderFactoryException(
                FILE_NOT_EXIST.format(path))

        try:
            return SKassenTransactionProvider(file_checker, path)
        except TransactionProviderException:
            pass

        try:
            return VrBankTransactionProvider(file_checker, path)
        except TransactionProviderException:
            pass

        raise TransactionProviderFactoryException(
            NOT_A_ACCOUNT_STATEMENT.format(path))
