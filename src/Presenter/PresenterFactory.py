from src.Configuration.PresenterConfig import PresenterConfig
from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.MultiPresenter import MultiPresenter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.PresenterFactoryException import PresenterFactoryException
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter


INVALID_INPUT = "no csv output nor pie chart presenter chosen"
PRESENTER_FACTORY_ERROR = "Presenter selection error|what:<{}>"


class PresenterFactory:
    def get(self, c: PresenterConfig) -> TransactionPresenter:
        try:
            if c.csv_presenter_enable and not c.savings_presenter_enable:
                return CsvPresenter(c.csv_output_file)

            elif c.savings_presenter_enable and not c.csv_presenter_enable:
                return SavingsPresenter(c.title, c.plotter, c.ignore_list)

            elif c.csv_presenter_enable and c.savings_presenter_enable:
                pres_list = [CsvPresenter(c.csv_output_file),
                             SavingsPresenter(c.title, c.plotter, c.ignore_list)]
                return MultiPresenter(pres_list)

        except PresenterException as e:
            msg = PRESENTER_FACTORY_ERROR.format(str(e))
            raise PresenterFactoryException(msg)

        msg = PRESENTER_FACTORY_ERROR.format(INVALID_INPUT)
        raise PresenterFactoryException(msg)
