from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.Plotter import Plotter
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter
from src.Sort.TransactionDict import TransactionDict


class MultiPresenter(TransactionPresenter):
    def __init__(self, path: str, title: str, plotter: Plotter, category_ignore_list: list[str]) -> None:

        self.pie_chart = plotter
        self.csv_presenter = CsvPresenter(path)
        self.savings_presenter = SavingsPresenter(
            title, self.pie_chart, category_ignore_list)

    def present(self, transaction_dict: TransactionDict) -> None:
        self.csv_presenter.present(transaction_dict)
        self.savings_presenter.present(transaction_dict)
