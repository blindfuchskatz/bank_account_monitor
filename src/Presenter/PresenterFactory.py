

import re
from src.CsvPattern import CSV_REGEX_PATTERN
from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.MultiPresenter import MultiPresenter
from src.Presenter.PieChart import PieChart
from src.Presenter.Plotter import Plotter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.PresenterFactoryException import PresenterFactoryException
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter


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

    def get_plotter(self) -> Plotter:
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
