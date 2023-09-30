import re
import unittest

from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionConverterException import TransactionConverterException
from utest.TestHelper import CustomAssert

someTransaction = "Mein GiroDirekt;DE1234567890;ABCDEF;VR BANK;31.08.2023;31.08.2023;Leasing Auto;DE987654321;ABCDEFGHIJ;Debit;Leasing;-1.310,90;EUR;1.234.567,89;;Drogeriemarkt;;DE52637485876800000123;OFFLINE"


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


class AVrBankTransactionConverter(unittest.TestCase):
    def setUp(self):
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionConverterException)
        self.c = VrBankTransactionConverter()

    def testConvertDate(self):
        t = self.c.convert(someTransaction)
        self.assertEqual(t.date, "31.08.2023")

    def testConvertType(self):
        t = self.c.convert(someTransaction)
        self.assertEqual(t.type, "Debit")

    def testConvertDesc(self):
        t = self.c.convert(someTransaction)
        self.assertEqual(t.desc, "Leasing")

    def testConvertValue(self):
        t = self.c.convert(someTransaction)
        self.assertEqual(t.value, -131090)

    def testRaiseExceptionWhenInvalidCsvLine(self):
        invalid_line_length = "a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r"

        self.ca.assertRaisesWithMessage(FORMAT_ERROR_TO_FEW_LINES.format(
            NUMBER_CSV_ENTRIES, 18), self.c.convert, invalid_line_length)

    def testRaiseExceptionWhenDateIsMissing(self):
        cate_missing = "a;b;c;d;e;f;g;h;i;debit;desc;-10.000,76;m;n;o;p;q;r;s"

        csv_line = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'debit',
                    'desc', '-10.000,76', 'm', 'n', 'o', 'p', 'q', 'r', 's']
        self.ca.assertRaisesWithMessage(FORMAT_ERROR_MISSING_DATE.format(
            csv_line), self.c.convert, cate_missing)

    def testRaiseExceptionWhenInvalidValue(self):
        invalid_value = "a;b;c;d;31.08.2023;f;g;h;i;debit;desc;{};m;n;o;p;q;r;s"

        self.ca.assertRaisesWithMessage(FORMAT_ERROR_VALUE.format(
            "j"), self.c.convert, invalid_value.format("j"))

        self.ca.assertRaisesWithMessage(FORMAT_ERROR_VALUE.format(
            "-10"), self.c.convert, invalid_value.format("-10"))

        self.ca.assertRaisesWithMessage(FORMAT_ERROR_VALUE.format(
            "-10,0"), self.c.convert, invalid_value.format("-10,0"))

        self.ca.assertRaisesWithMessage(FORMAT_ERROR_VALUE.format(
            "10.01"), self.c.convert, invalid_value.format("10.01"))
