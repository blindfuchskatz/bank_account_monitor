import re
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionConverterException import TransactionConverterException


FORMAT_ERROR_TO_FEW_LINES = "VR bank converter illegal csv format|expected elements:{}|actual elements:{}>"
FORMAT_ERROR_MISSING_DATE = "VR bank converter illegal csv format|what:<date is missing>|line entries:{}"
FORMAT_ERROR_VALUE = "VR bank converter illegal csv format|what:<invalid value format>|value:{}"

NUMBER_CSV_ENTRIES = 19


class VrBankTransactionConverter:
    def convert(self, transaction_string):
        regex_patter = r'(?:^|;)(?:"([^"]*(?:""[^"]*)*)"|([^";]*))'

        matches = re.findall(regex_patter, transaction_string)
        csv_list = [match[0] or match[1] for match in matches]

        if len(csv_list) < NUMBER_CSV_ENTRIES:
            e = FORMAT_ERROR_TO_FEW_LINES.format(
                NUMBER_CSV_ENTRIES, len(csv_list))
            raise TransactionConverterException(e)

        t_date = self.__get_date(csv_list)
        t_type = self.__get_type(csv_list)
        t_desc = self.__get_desc(csv_list)
        t_value = self.__get_value(csv_list)

        return Transaction(t_date, t_type, t_desc, t_value)

    def __get_date(self, csv_list):
        regex_pattern = r"^(\d{2}\.\d{2}\.\d{4})"
        if re.findall(regex_pattern, csv_list[4]):
            return csv_list[4]
        else:
            e = FORMAT_ERROR_MISSING_DATE.format(csv_list)
            raise TransactionConverterException(e)

    def __get_type(self, csv_list):
        return csv_list[9]

    def __get_desc(self, csv_list):
        return csv_list[10]

    def __get_value(self, csv_list):
        value_str = csv_list[11]
        regex_pattern = r"(-?.+,\d{2}$)"

        if re.findall(regex_pattern, value_str):
            cleaned_string = value_str.replace(".", "")
            cleaned_string = cleaned_string.replace(",", "")
            return int(cleaned_string)
        else:
            e = FORMAT_ERROR_VALUE.format(value_str)
            raise TransactionConverterException(e)
