import re
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionConverterException import TransactionConverterException

TRANSACTION_FORMAT_ERROR = "SKassen converter illegal transaction format|{} is missing|transaction:<{}>"


class SKassenTransactionConverter:
    def convert(self, transaction_string: str) -> Transaction:
        t_date = self.__get_date(transaction_string)
        t_type = self.__get_type(transaction_string)
        t_desc = self.__get_description(transaction_string)
        t_value = self.__get_value(transaction_string)

        return Transaction(t_date, t_type, t_desc, t_value)

    def __get_date(self, transaction_string):
        regex_pattern = r"^(\d{2}\.\d{2}\.\d{4})"
        return self.__get_transaction_element(
            transaction_string, regex_pattern, "date")

    def __get_type(self, transaction_string):
        regex_pattern = r"((?<= )[^\n]*(?=\n))"
        return self.__get_transaction_element(
            transaction_string, regex_pattern, "type")

    def __get_description(self, transaction_string):
        regex_pattern = r"((?<=\n)[\s\S]+?(?= {4,}))"
        return self.__get_transaction_element(
            transaction_string, regex_pattern, "description")

    def __get_value(self, transaction_string):
        regex_pattern = r"( {4,}-?.+,\d{2}$)"
        value_str = self.__get_transaction_element(
            transaction_string, regex_pattern, "value")

        cleaned_string = value_str.replace(".", "")
        cleaned_string = cleaned_string.replace(",", "")
        return int(cleaned_string)

    def __get_transaction_element(self, transaction_string, regex_pattern, element):
        match = re.findall(regex_pattern, transaction_string)

        if match and match[0].strip():
            return match[0]
        else:
            raise TransactionConverterException(
                TRANSACTION_FORMAT_ERROR.format(element, transaction_string))
