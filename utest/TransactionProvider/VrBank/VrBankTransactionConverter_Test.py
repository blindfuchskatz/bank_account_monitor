import unittest

from src.TransactionProvider.TransactionConverterException import TransactionConverterException
from src.TransactionProvider.VrBank.VrBankTransactionConverter import FORMAT_ERROR_MISSING_DATE, FORMAT_ERROR_TO_FEW_LINES, FORMAT_ERROR_VALUE, NUMBER_CSV_ENTRIES, VrBankTransactionConverter
from utest.TestHelper import CustomAssert

someTransaction = "Mein GiroDirekt;DE1234567890;ABCDEF;VR BANK;31.08.2023;31.08.2023;Leasing Auto;DE987654321;ABCDEFGHIJ;Debit;Leasing;-1.310,90;EUR;1.234.567,89;;Drogeriemarkt;;DE52637485876800000123;OFFLINE"


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
        date_missing = "a;b;c;d;e;f;g;h;i;debit;desc;-10.000,76;m;n;o;p;q;r;s"

        csv_line = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'debit',
                    'desc', '-10.000,76', 'm', 'n', 'o', 'p', 'q', 'r', 's']
        self.ca.assertRaisesWithMessage(FORMAT_ERROR_MISSING_DATE.format(
            csv_line), self.c.convert, date_missing)

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
