from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.MultiPresenter import MultiPresenter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.PresenterFactoryException import PresenterFactoryException
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter
from src.Presenter.PresenterFactoryConfig import PresenterFactoryConfig


INVALID_INPUT = "no csv output nor pie chart presenter chosen"
PRESENTER_FACTORY_ERROR = "Presenter selection error|what:<{}>"


class PresenterFactory:
    def get(self, config: PresenterFactoryConfig) -> TransactionPresenter:
        try:
            if config.csv_output_file and not config.title:
                return CsvPresenter(config.csv_output_file)

            elif config.title and not config.csv_output_file:
                return SavingsPresenter(config.title, config.plotter,
                                        config.ignore_list)
            elif config.title and config.csv_output_file:
                return MultiPresenter(config.csv_output_file, config.title,
                                      config.plotter, config.ignore_list)

        except PresenterException as e:
            msg = PRESENTER_FACTORY_ERROR.format(str(e))
            raise PresenterFactoryException(msg)

        msg = PRESENTER_FACTORY_ERROR.format(INVALID_INPUT)
        raise PresenterFactoryException(msg)
