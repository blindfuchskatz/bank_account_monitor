from abc import abstractmethod


class TransactionPresenter:
    @abstractmethod
    def present(self, transaction_dict):
        pass
