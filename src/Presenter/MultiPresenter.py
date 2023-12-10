from typing import List
from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.Plotter import Plotter
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter
from src.Sort.TransactionDict import TransactionDict


class MultiPresenter(TransactionPresenter):
    def __init__(self, presenter_list: List[TransactionPresenter]) -> None:
        self.presenter_list = presenter_list

    def present(self, transaction_dict: TransactionDict) -> None:
        for presenter in self.presenter_list:
            presenter.present(transaction_dict)
