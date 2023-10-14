from src.File.FileChecker import FileChecker
from src.TransactionProvider.Factory import Factory
from src.TransactionProvider.MultiTransactionProvider import MultiTransactionProvider
from src.TransactionProvider.SKasse.SKassenTransactionProvider import SKassenTransactionProvider
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.TransactionProviderFactoryException import TransactionProviderFactoryException
from src.TransactionProvider.VrBank.VrBankTransactionProvider import VrBankTransactionProvider

NOT_A_ACCOUNT_STATEMENT = "Not supported bank account statement file|file:<{}>"
FILE_NOT_EXIST = "Account statement file does not exist:<{}>"


class TransactionProviderFactory(Factory):
    def get_transaction_provider(self, path: str) -> TransactionProvider:

        try:
            if (MultiTransactionProvider(path, self).is_needed()):
                return MultiTransactionProvider(path, self)

            if not self.file_exists(path):
                what = FILE_NOT_EXIST.format(path)
                raise TransactionProviderFactoryException(what)

            if SKassenTransactionProvider(path).is_account_statement():
                return SKassenTransactionProvider(path)

            if VrBankTransactionProvider(path).is_account_statement():
                return VrBankTransactionProvider(path)

        except TransactionProviderException:
            pass

        what = NOT_A_ACCOUNT_STATEMENT.format(path)
        raise TransactionProviderFactoryException(what)

    def file_exists(self, path: str) -> bool:
        return FileChecker.file_exists(path)
