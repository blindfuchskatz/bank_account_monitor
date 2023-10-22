import re
import unittest
from unittest.mock import MagicMock
from src.CsvPattern import CSV_REGEX_PATTERN

from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.PieChart import PieChart
from src.Presenter.Plotter import Plotter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter

from utest.TestHelper import CustomAssert


class PresenterFactoryException(Exception):
    """Raised on presenter factory error"""


class MultiPresenter(TransactionPresenter):
    def __init__(self, path: str, title: str, plotter: Plotter, category_ignore_list: list[str]) -> None:

        self.pie_chart = plotter
        self.csv_presenter = CsvPresenter(path)
        self.savings_presenter = SavingsPresenter(
            title, self.pie_chart, category_ignore_list)

    def present(self, transaction_dict):
        self.csv_presenter.present(transaction_dict)
        self.savings_presenter.present(transaction_dict)


INVALID_INPUT = "no csv output nor pie chart presenter chosen"
PRESENTER_FACTORY_ERROR = "Presenter selection error|what:<{}>"


class PresenterFactory:
    def __init__(self) -> None:
        self.plotter = PieChart()

    def get(self, csv_output_file: str, plotter_data: str) -> TransactionPresenter:
        try:
            if csv_output_file and not plotter_data:
                return CsvPresenter(csv_output_file)
            elif plotter_data and not csv_output_file:
                t, i = self.__separate_title_and_ignore_list(plotter_data)
                return SavingsPresenter(t, self.plotter, i)
            elif plotter_data and csv_output_file:
                t, i = self.__separate_title_and_ignore_list(plotter_data)
                return MultiPresenter(csv_output_file, t, self.plotter, i)

        except PresenterException as e:
            msg = PRESENTER_FACTORY_ERROR.format(str(e))
            raise PresenterFactoryException(msg)

        msg = PRESENTER_FACTORY_ERROR.format(INVALID_INPUT)
        raise PresenterFactoryException(msg)

    def get_plotter(self):
        return self.plotter

    def __separate_title_and_ignore_list(self, plotter_data):
        category_ignore_list = []
        title = ""

        matches = re.findall(CSV_REGEX_PATTERN, plotter_data)
        csv_list = [match[0] or match[1] for match in matches]

        if len(csv_list) == 1:
            return csv_list[0], []

        title = csv_list[0]
        for entry in csv_list[1:]:
            category_ignore_list.append(entry)

        return title, category_ignore_list


SOME_PATH = "some/path"
TITLE = "title"


class APresenterFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.cvs_presenter_init = CsvPresenter.__init__
        CsvPresenter.__init__ = MagicMock(return_value=None)

        self.savings_presenter_init = SavingsPresenter.__init__
        SavingsPresenter.__init__ = MagicMock(return_value=None)

        self.ca = CustomAssert()
        self.ca.setExceptionType(PresenterFactoryException)
        self.f = PresenterFactory()

    def tearDown(self) -> None:
        CsvPresenter.__init__ = self.cvs_presenter_init
        SavingsPresenter.__init__ = self.savings_presenter_init

    def testReturnCsvPresenter(self):
        p = self.f.get(SOME_PATH, "")

        self.assertEqual(type(p), CsvPresenter)
        CsvPresenter.__init__.assert_called_with(SOME_PATH)

    def testReturnSavingsPresenter(self):
        plotter = self.f.get_plotter()

        p = self.f.get("", TITLE)

        self.assertEqual(type(p), SavingsPresenter)
        SavingsPresenter.__init__.assert_called_with(TITLE,  plotter, [])

    def testConsiderCategoryIgnoreListForSavingsPresenter(self):
        plotter = self.f.get_plotter()

        p = self.f.get("", "title;fund")

        self.assertEqual(type(p), SavingsPresenter)
        SavingsPresenter.__init__.assert_called_with(TITLE,  plotter, ["fund"])

    def testReturnMultiPresenter(self):
        plotter = self.f.get_plotter()

        p = self.f.get(SOME_PATH, TITLE)

        self.assertEqual(type(p), MultiPresenter)
        CsvPresenter.__init__.assert_called_with(SOME_PATH)
        SavingsPresenter.__init__.assert_called_with(TITLE,  plotter, [])

    def testConsiderCategoryIgnoreListForMultiPresenter(self):
        plotter = self.f.get_plotter()

        p = self.f.get(SOME_PATH, "title;fund;bank")

        self.assertEqual(type(p), MultiPresenter)
        CsvPresenter.__init__.assert_called_with(SOME_PATH)
        SavingsPresenter.__init__.assert_called_with(
            TITLE,  plotter, ["fund", "bank"])

    def testRaiseExceptionWhenNoPresenterChosen(self):
        msg = PRESENTER_FACTORY_ERROR.format(INVALID_INPUT)
        self.ca.assertRaisesWithMessage(msg, self.f.get, "", "")

    def testForwardPresenterExceptions(self):
        CsvPresenter.__init__ = MagicMock(side_effect=PresenterException("e"))
        msg = PRESENTER_FACTORY_ERROR.format("e")
        self.ca.assertRaisesWithMessage(msg, self.f.get, SOME_PATH, "")
