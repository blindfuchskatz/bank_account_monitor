from abc import ABC, abstractmethod

from src.Sort.TransactionDict import TransactionDict


class TransactionPresenter(ABC):
    @abstractmethod
    def present(self, transaction_dict: TransactionDict):
        pass  # pragma: no cover
