import unittest
from src.TransactionProvider.TransactionConverterException import TransactionConverterException
from src.TransactionProvider.SKasse.SKassenTransactionConverter import SKassenTransactionConverter
from src.TransactionProvider.SKasse.SKassenTransactionConverter import TRANSACTION_FORMAT_ERROR
from utest.TestHelper import CustomAssert

someTransaction = """31.08.2023 Entgeltabrechnung / Wert: 01.09.2023
siehe Anlage Nr. 1               -6,90"""

someGutschrift = """31.08.2023 Gutschrift
mercy               6,90"""

someBigGutschrift = """31.08.2023 Gutschrift
mercy       10.000.000,90"""

transactionWithoutDate = "string contains no date"

transactionDateNotInFront = """Entgeltabrechnung / Wert: 01.09.2023
siehe Anlage Nr. 1               -6,90"""

transactionWithoutType = """31.08.2023 Entgeltabrechnung / Wert: 01.09.2023 siehe Anlage Nr. 1               -6,90"""
transactionWithoutDescription = """31.08.2023 Entgeltabrechnung / Wert: 01.09.2023
               -6,90"""

transactionWithoutValue = """31.08.2023 Entgeltabrechnung / Wert: 01.09.2023
siehe Anlage Nr. 1               8,0"""


class ASKassenTransactionConverter(unittest.TestCase):
    def setUp(self):
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionConverterException)

    def testConvertDate(self):
        c = SKassenTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.date, "31.08.2023")

    def testRaiseExceptionWhenDateNotExist(self):
        c = SKassenTransactionConverter()
        self.ca.assertRaisesWithMessage(TRANSACTION_FORMAT_ERROR.format(
            "date", transactionWithoutDate), c.convert, transactionWithoutDate)

    def testRaiseExceptionWhenTransactionStringStartNotWithDate(self):
        c = SKassenTransactionConverter()
        self.ca.assertRaisesWithMessage(TRANSACTION_FORMAT_ERROR.format(
            "date", transactionDateNotInFront), c.convert, transactionDateNotInFront)

    def testConvertType(self):
        c = SKassenTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.type, "Entgeltabrechnung / Wert: 01.09.2023")

    def testRaiseExceptionWhenTypeIsMissing(self):
        c = SKassenTransactionConverter()
        self.ca.assertRaisesWithMessage(TRANSACTION_FORMAT_ERROR.format(
            "type", transactionWithoutType), c.convert, transactionWithoutType)

    def testConvertDescription(self):
        c = SKassenTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.desc, "siehe Anlage Nr. 1")

    def testRaiseExceptionWhenDescriptionIsMissing(self):
        c = SKassenTransactionConverter()
        self.ca.assertRaisesWithMessage(TRANSACTION_FORMAT_ERROR.format(
            "description", transactionWithoutDescription), c.convert, transactionWithoutDescription)

    def testConvertNegativeValue(self):
        c = SKassenTransactionConverter()
        t = c.convert(someTransaction)
        self.assertEqual(t.value, -690)

    def testConvertPositiveValue(self):
        c = SKassenTransactionConverter()
        t = c.convert(someGutschrift)
        self.assertEqual(t.value, 690)

    def testConvertValueGermanNumberformat(self):
        c = SKassenTransactionConverter()
        t = c.convert(someBigGutschrift)
        self.assertEqual(t.value, 1000000090)

    def testRaiseExceptionWhenValueIsMissing(self):
        c = SKassenTransactionConverter()
        self.ca.assertRaisesWithMessage(TRANSACTION_FORMAT_ERROR.format(
            "value", transactionWithoutValue), c.convert, transactionWithoutValue)
