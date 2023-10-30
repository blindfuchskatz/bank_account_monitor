import unittest
from unittest.mock import MagicMock
from src.File.FileChecker import FileChecker
from src.Logger import Logger


from src.Sort.SortRule import SortRule
from src.Sort.SortRuleProvider import SortRuleProvider
from src.Sort.SortRuleProviderException import SortRuleProviderException
from src.TransactionProvider.Transaction import Transaction
from src.TransactionMonitor import TransactionMonitor
from src.Presenter.TransactionPresenter import TransactionPresenter
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.Sort.TransactionSorter import TransactionSorter
from src.Sort.TransactionSorterException import TransactionSorterException

t_insurance = Transaction("12.01.2023", "debit", "HUK wants money", -45356)
t_car = Transaction("23.04.2023", "debit", "Shell wants money", -9643)
t_gez = Transaction("07.05.2023", "debit", "GEZ wants fucking money", -5443)


r_insurance = SortRule("Insurance", ["HUK"])
r_car = SortRule("Car", ["Shell"])

trans_dict = {"Insurance": [t_insurance], "Car": [t_car], "misc": [t_gez]}

error_msg = "some error"


class TransactionProviderStub(TransactionProvider):

    def get_transactions(self):
        return  # pragma: no cover


class SortRuleProviderStub(SortRuleProvider):
    def get_sort_rules(self):
        return  # pragma: no cover


class TransactionPresenterStub(TransactionPresenter):
    def present(self):
        return  # pragma: no cover


class ATransactionMonitor(unittest.TestCase):
    def setUp(self) -> None:
        self.t_provider = TransactionProviderStub()
        self.sr_provider = SortRuleProviderStub()
        self.t_presenter = TransactionPresenterStub()
        self.logger = Logger()
        self.sorter = TransactionSorter()
        self.tm = TransactionMonitor(
            self.t_provider, self.sr_provider, self.sorter, self.t_presenter, self.logger)

    def testPresentSortedTransactions(self):

        self.t_provider.get_transactions = MagicMock(
            return_value=[t_insurance, t_car, t_gez])

        self.sr_provider.get_sort_rules = MagicMock(
            return_value=[r_insurance, r_car])

        self.t_presenter.present = MagicMock()

        self.tm.monitor()

        self.t_provider.get_transactions.assert_called_once()
        self.sr_provider.get_sort_rules.assert_called_once()
        self.t_presenter.present.assert_called_once_with(trans_dict)

    def testPrintTransactionProviderExceptions(self):

        self.t_provider.get_transactions = MagicMock(
            side_effect=TransactionProviderException(error_msg))
        self.logger.error = MagicMock()

        self.tm.monitor()

        self.logger.error.assert_called_once_with(error_msg)

    def testPrintSortRuleProviderExceptions(self):

        self.t_provider.get_transactions = MagicMock(return_value=[])

        self.sr_provider.get_sort_rules = MagicMock(
            side_effect=SortRuleProviderException(error_msg))

        self.logger.error = MagicMock()

        self.tm.monitor()

        self.logger.error.assert_called_once_with(error_msg)

    def testPrintPresenterExceptions(self):

        self.t_provider.get_transactions = MagicMock(return_value=[])
        self.sr_provider.get_sort_rules = MagicMock(return_value=[])
        self.t_presenter.present = MagicMock(
            side_effect=SortRuleProviderException(error_msg))

        self.logger.error = MagicMock()

        self.tm.monitor()

        self.logger.error.assert_called_once_with(error_msg)

    def testPrintTransactionSorterExceptions(self):

        self.t_provider.get_transactions = MagicMock(return_value=[])
        self.sr_provider.get_sort_rules = MagicMock(return_value=[])
        self.t_presenter.present = MagicMock()
        self.sorter.sort = MagicMock(
            side_effect=TransactionSorterException(error_msg))

        self.logger.error = MagicMock()

        self.tm.monitor()

        self.logger.error.assert_called_once_with(error_msg)
