import unittest
from unittest.mock import MagicMock
from src.Presenter.MultiPresenter import MultiPresenter

from src.Presenter.TransactionPresenter import TransactionPresenter
from src.Sort.TransactionDict import TransactionDict


class PresenterStub1(TransactionPresenter):
    def present(self, transaction_dict: TransactionDict) -> None:
        return  # pragma: no cover


class PresenterStub2(TransactionPresenter):
    def present(self, transaction_dict: TransactionDict) -> None:
        return  # pragma: no cover


class PresenterStub3(TransactionPresenter):
    def present(self, transaction_dict: TransactionDict) -> None:
        return  # pragma: no cover


class AMultiPresenter(unittest.TestCase):
    def testExecuteAllPresentersInList(self):
        p1 = PresenterStub1()
        p2 = PresenterStub2()
        p3 = PresenterStub3()

        p1.present = MagicMock()
        p2.present = MagicMock()
        p3.present = MagicMock()

        pres_list = [p1, p2, p3]
        multi_pres = MultiPresenter(pres_list)

        multi_pres.present({})

        p1.present.assert_called_once_with({})
        p2.present.assert_called_once_with({})
        p3.present.assert_called_once_with({})
