import unittest
from unittest.mock import MagicMock

from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.MultiPresenter import MultiPresenter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.PresenterFactory import INVALID_INPUT, PRESENTER_FACTORY_ERROR, PresenterFactory
from src.Presenter.PresenterFactoryException import PresenterFactoryException
from src.Presenter.SavingsPresenter import SavingsPresenter

from utest.TestHelper import CustomAssert

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
