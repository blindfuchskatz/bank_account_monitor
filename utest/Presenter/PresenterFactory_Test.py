import unittest
from unittest.mock import MagicMock
from src.Configuration.PresenterConfig import CvePresConfig, PresenterId, SavingsPresConfig

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
        conf = {PresenterId.cve: CvePresConfig(csv_output_file=SOME_PATH)}

        p = self.f.get(conf)

        self.assertEqual(type(p), CsvPresenter)
        CsvPresenter.__init__.assert_called_with(SOME_PATH)

    def testReturnSavingsPresenter(self):
        save_conf = SavingsPresConfig(title=TITLE, ignore_list=["fund"])
        conf = {PresenterId.savings: save_conf}

        p = self.f.get(conf)

        self.assertEqual(type(p), SavingsPresenter)
        SavingsPresenter.__init__.assert_called_with(save_conf)

    def testReturnMultiPresenter(self):
        cve_conf = CvePresConfig(csv_output_file=SOME_PATH)
        save_conf = SavingsPresConfig(title=TITLE, ignore_list=[])
        conf = {PresenterId.cve: cve_conf, PresenterId.savings: save_conf}

        p = self.f.get(conf)

        self.assertEqual(type(p), MultiPresenter)
        CsvPresenter.__init__.assert_called_with(SOME_PATH)
        SavingsPresenter.__init__.assert_called_with(save_conf)

    def testConsiderCategoryIgnoreListForMultiPresenter(self):
        c_conf = CvePresConfig(csv_output_file=SOME_PATH)
        s_conf = SavingsPresConfig(title=TITLE, ignore_list=["fund", "bank"])
        conf = {PresenterId.cve: c_conf, PresenterId.savings: s_conf}

        p = self.f.get(conf)

        self.assertEqual(type(p), MultiPresenter)
        CsvPresenter.__init__.assert_called_with(SOME_PATH)
        SavingsPresenter.__init__.assert_called_with(s_conf)

    def testRaiseExceptionWhenNoPresenterChosen(self):
        conf = {}
        msg = PRESENTER_FACTORY_ERROR.format(INVALID_INPUT)

        self.ca.assertRaisesWithMessage(msg, self.f.get, conf)

    def testForwardPresenterExceptions(self):
        conf = {PresenterId.cve: CvePresConfig(csv_output_file=SOME_PATH)}
        CsvPresenter.__init__ = MagicMock(side_effect=PresenterException("e"))
        msg = PRESENTER_FACTORY_ERROR.format("e")

        self.ca.assertRaisesWithMessage(msg, self.f.get, conf)
