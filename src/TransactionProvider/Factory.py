from abc import abstractmethod

from src.TransactionProvider.TransactionProvider import TransactionProvider


class Factory:
    @abstractmethod
    def get_transaction_provider(self, path: str) -> TransactionProvider:
        pass
