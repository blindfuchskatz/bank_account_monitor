from abc import ABC, abstractmethod

from src.TransactionProvider.TransactionProvider import TransactionProvider


class Factory(ABC):
    @abstractmethod
    def get_transaction_provider(self, path: str) -> TransactionProvider:
        pass  # pragma: no cover
