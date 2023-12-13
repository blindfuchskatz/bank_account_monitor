from typing import List
from src.Configuration.PresenterConfig import SavingsPresConfig
from src.Presenter.Plotter import Plotter
from src.Presenter.TransactionPresenter import TransactionPresenter

from src.Sort.TransactionDict import TransactionDict
from src.TransactionProvider.Transaction import Transaction


class SavingsPresenter(TransactionPresenter):
    def __init__(self, conf: SavingsPresConfig) -> None:
        self.__plotter = conf.plotter
        self.__path = conf.plot_output_file
        self.__title = conf.title
        self.__ignore_list = conf.ignore_list

    def present(self, transaction_dict: TransactionDict) -> None:

        if not transaction_dict:
            return

        cleaned_dict = self.__remove_ignored_categories(transaction_dict)
        plot_dict = self.__calc_savings(cleaned_dict)

        negative_trans_dict = self.__get_negative_trans_dict(cleaned_dict)

        for category, transaction_list in negative_trans_dict.items():
            value = self.__calc_sum(transaction_list)
            plot_dict[category] = abs(value)

        self.__plotter.plot(self.__title, plot_dict, self.__path)

    def __remove_ignored_categories(self, transaction_dict: TransactionDict):
        cleaned_dict = {}
        for category, transaction_list in transaction_dict.items():
            if category in self.__ignore_list:
                continue
            cleaned_dict[category] = transaction_list

        return cleaned_dict

    def __calc_savings(self, transaction_dict: TransactionDict):
        savings = 0
        plot_dict = {}

        for transaction_list in transaction_dict.values():
            savings += self.__calc_sum(transaction_list)

        if savings < 0:
            plot_dict["Losings"] = abs(savings)
        else:
            plot_dict["Savings"] = savings

        return plot_dict

    def __calc_sum(self, transaction_list: List[Transaction]):
        calc_sum = 0

        for t in transaction_list:
            calc_sum += t.value

        return calc_sum

    def __get_negative_trans_dict(self, transaction_dict: TransactionDict):
        negative_trans_dict = {}

        for category, transaction_list in transaction_dict.items():
            nt_list = self.__get_negative_trans_list(transaction_list)

            if nt_list:
                negative_trans_dict[category] = nt_list

        return negative_trans_dict

    def __get_negative_trans_list(self, transaction_list: List[Transaction]):
        nt_list = []

        for t in transaction_list:
            if t.value < 0:
                nt_list.append(t)
        return nt_list
