
from abc import abstractmethod

INVALID_INPUT_PATH = "{} transaction provider error|invalid input path|path:<{}>"


class TransactionProvider:
    @abstractmethod
    def get_transactions(self):
        pass
