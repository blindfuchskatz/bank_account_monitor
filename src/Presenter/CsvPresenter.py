from src.File.FileChecker import FileChecker
from src.File.FileWriter import FileWriter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.TransactionPresenter import TransactionPresenter
from src.Sort.TransactionDict import TransactionDict

INVALID_INPUT_PATH = "Cve presenter error|invalid input path|path:<{}>"
NO_PATH = "Cve presenter error|no input path"


class CsvPresenter(TransactionPresenter):
    def __init__(self, input_path: str) -> None:
        self.__path = input_path

        if not self.__path:
            raise PresenterException(NO_PATH)
        elif not FileChecker.dir_of_file_exists(self.__path):
            raise PresenterException(INVALID_INPUT_PATH.format(self.__path))

    def present(self, transaction_dict: TransactionDict) -> None:
        csv_out = ""

        for category, transaction_list in transaction_dict.items():
            csv_out += self.__transform_category_to_csv(
                category, transaction_list)

        FileWriter.write(self.__path, csv_out.strip())

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
