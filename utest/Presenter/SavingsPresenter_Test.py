from typing import Dict
import unittest

from unittest.mock import MagicMock
from src.Presenter.Plotter import Plotter
from src.Presenter.SavingsPresenter import SavingsPresenter

from src.TransactionProvider.Transaction import Transaction

t_n1 = Transaction("d1", "t1", "a", -1)
t_p2 = Transaction("d2", "t2", "b", 2)
t_n3 = Transaction("d3", "t3", "c", -3)
t_p10 = Transaction("d4", "t4", "d", 10)
t_n9 = Transaction("d4", "t4", "d", -9)


class PieChartStub(Plotter):
    def plot(self, title: str, data_dict: Dict):
        """Stub for testing"""
        pass  # pragma: no cover


class ASavingsPresenter(unittest.TestCase):
    def setUp(self) -> None:
        self.pie_chart = PieChartStub()
        self.pie_chart.plot = MagicMock()
        self.p = SavingsPresenter("title", self.pie_chart, [])

    def testCalcSavings(self):
        t_dict = {"misc": [t_n1, t_p2],
                  "car": [t_n3],
                  "salary": [t_p10]}

        self.p.present(t_dict)

        plot_dict = {'Savings': 8, 'misc': 1, 'car': 3}
        self.pie_chart.plot.assert_called_once_with("title", plot_dict)

    def testCalcLoses(self):
        t_dict = {"misc": [t_n1, t_p2],
                  "car": [t_n3, t_n9],
                  "salary": [t_p10]}

        self.p.present(t_dict)

        plot_dict = {'Losings': 1, 'misc': 1, 'car': 12}
        self.pie_chart.plot.assert_called_once_with("title", plot_dict)

    def testIgnoreCategories(self):
        t_dict = {"misc": [t_n1, t_p2],
                  "car": [t_n3],
                  "insurance": [],
                  "funds": [t_n9],
                  "gold": [t_n1],
                  "salary": [t_p10]}

        p = SavingsPresenter("title", self.pie_chart, ["funds", "gold"])

        p.present(t_dict)

        plot_dict = {'Savings': 8, 'misc': 1, 'car': 3}
        self.pie_chart.plot.assert_called_once_with("title", plot_dict)

    def testCalcOnlyLosings(self):
        t_dict = {"misc": [t_n1, t_n3]}

        p = SavingsPresenter("title", self.pie_chart, [])

        p.present(t_dict)

        plot_dict = {'Losings': 4, 'misc': 4}
        self.pie_chart.plot.assert_called_once_with("title", plot_dict)

    def testDoNothing(self):
        t_dict = {}

        self.p.present(t_dict)

        self.pie_chart.plot.assert_not_called()

    def testCalcEmptyTransactionDict(self):
        t_dict = {"misc": []}

        self.p.present(t_dict)

        plot_dict = {'Savings': 0}
        self.pie_chart.plot.assert_called_once_with("title", plot_dict)
