import re
import unittest

from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionConverterException import TransactionConverterException
from utest.TestHelper import CustomAssert

someTransaction = "Mein GiroDirekt;DE1234567890;ABCDEF;VR BANK;31.08.2023;31.08.2023;Leasing Auto;DE987654321;ABCDEFGHIJ;Debit;Leasing;-1.310,90;EUR;1.234.567,89;;Drogeriemarkt;;DE52637485876800000123;OFFLINE"

invalidCsvLine = "a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r"

TRANSACTION_FORMAT_ERROR = "VR bank converter illegal csv format|expected elements:{}|actual elements:{}>"
NUMBER_CSV_ENTRIES = 19


class VrBankTransactionConverter:
    def convert(self, transaction_string):
        regex_patter = r'(?:^|;)(?:"([^"]*(?:""[^"]*)*)"|([^";]*))'

        matches = re.findall(regex_patter, transaction_string)
        csv_list = [match[0] or match[1] for match in matches]

        if len(csv_list) < NUMBER_CSV_ENTRIES:
            e = TRANSACTION_FORMAT_ERROR.format(
                NUMBER_CSV_ENTRIES, len(csv_list))
            raise TransactionConverterException(e)

        t_date = self.__get_date(csv_list)
        t_type = self.__get_type(csv_list)
        t_desc = self.__get_desc(csv_list)
        t_value = self.__get_value(csv_list)

        return Transaction(t_date, t_type, t_desc, t_value)

    def __get_date(self, csv_list):
        return csv_list[4]

    def __get_type(self, csv_list):
        return csv_list[9]

    def __get_desc(self, csv_list):
        return csv_list[10]

    def __get_value(self, csv_list):
        value_str = csv_list[11]
        cleaned_string = value_str.replace(".", "")
        cleaned_string = cleaned_string.replace(",", "")
        return int(cleaned_string)


class AVrBankTransactionConverter(unittest.TestCase):
    def setUp(self):
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionConverterException)

    def testConvertDate(self):
        c = VrBankTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.date, "31.08.2023")

    def testConvertType(self):
        c = VrBankTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.type, "Debit")

    def testConvertDesc(self):
        c = VrBankTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.desc, "Leasing")

    def testConvertValue(self):
        c = VrBankTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.value, -131090)

    def testRaiseExceptionWhenInvalidCsvLine(self):
        c = VrBankTransactionConverter()
        self.ca.assertRaisesWithMessage(TRANSACTION_FORMAT_ERROR.format(
            NUMBER_CSV_ENTRIES, 18), c.convert, invalidCsvLine)
