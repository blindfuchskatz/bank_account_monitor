from abc import abstractmethod

from src.Sort.TransactionDict import TransactionDict


class TransactionPresenter:
    @abstractmethod
    def present(self, transaction_dict: TransactionDict):
        pass
