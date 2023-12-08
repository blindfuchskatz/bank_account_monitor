import re
from src.CsvPattern import CSV_REGEX_PATTERN
from src.Presenter.PresenterFactoryConfig import PresenterFactoryConfig


class UiConfigTranslator:
    def translate(self, csv_output_file: str,
                  plotter_data_csv: str) -> PresenterFactoryConfig:

        t, i_list = self.__separate_title_and_ignore_list(plotter_data_csv)
        trans_conf = PresenterFactoryConfig(csv_output_file=csv_output_file,
                                            title=t,
                                            ignore_list=i_list)

        return trans_conf

    def __separate_title_and_ignore_list(self, plotter_data_csv):
        category_ignore_list = []
        title = ""

        matches = re.findall(CSV_REGEX_PATTERN, plotter_data_csv)
        csv_list = [match[0] or match[1] for match in matches]

        if len(csv_list) == 1:
            return csv_list[0], []

        title = csv_list[0]
        for entry in csv_list[1:]:
            category_ignore_list.append(entry)

        return title, category_ignore_list
