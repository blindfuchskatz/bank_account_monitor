
from abc import abstractmethod


class TransactionProvider:
    @abstractmethod
    def get_transactions(self):
        pass
