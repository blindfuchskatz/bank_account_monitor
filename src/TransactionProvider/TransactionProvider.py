
from abc import ABC, abstractmethod

INVALID_INPUT_PATH = "{} transaction provider error|invalid input path|path:<{}>"


class TransactionProvider(ABC):
    @abstractmethod
    def get_transactions(self):
        pass  # pragma: no cover
