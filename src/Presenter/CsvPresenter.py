from src.Presenter.PresenterException import PresenterException
from src.Presenter.TransactionPresenter import TransactionPresenter

INVALID_INPUT_PATH = "Cve presenter error|invalid input path|path:<{}>"
NO_PATH = "Cve presenter error|no input path"


class CsvPresenter(TransactionPresenter):
    def __init__(self, file_checker, file_writer, input_path) -> None:
        self.__file_checker = file_checker
        self.__file_writer = file_writer
        self.__path = input_path

        if not self.__path:
            raise PresenterException(NO_PATH)
        elif not self.__file_checker.dir_of_file_exists(self.__path):
            raise PresenterException(INVALID_INPUT_PATH.format(self.__path))

    def present(self, transaction_dict):
        csv_out = ""

        for category, transaction_list in transaction_dict.items():
            csv_out += self.__transform_category_to_csv(
                category, transaction_list)

        self.__file_writer.write(self.__path, csv_out.strip())

    def __transform_category_to_csv(self, category, transaction_list):
        category_out = ""
        csv_format_str = "{};{};{};\"{}\";{}\n"

        if not transaction_list:
            return category + ";\n"

        for t in transaction_list:
            csv_line = csv_format_str.format(
                category, t.date, t.type, t.desc, "{:.2f}".format(t.value / 100.0))

            category_out += csv_line

        return category_out
