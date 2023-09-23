import unittest
from src.TransactionProvider.SKasse.SKassenTransactionExtractor import SKassenTransactionExtractor

noTransaction = """text
Kontostand am 31.07.2023, text text text Nr.    7            0,00
 ,  09421/863-0
text
text
text"""

statementAccount = """ Kontostand am 31.07.2023, text text text text            0,00
21.08.2023 Credit
description first line
description second line              100.000,09
text
text
text
31.08.2023 Debit
description               -6,90
text
text
31.08.2023 Debit
description first line
description second line               -5,83
Kontostand am 31.08.2023 um 20:02 Uhr             800.730,22
text
text
text
vom 01.08.2023 bis 31.08.2023                               6,90-
                text    6,90                6,90-
                                                            --------------
 31.08.2023                                                6,90-
text
text
text
."""

transactionCredit = """21.08.2023 Credit
description first line
description second line              100.000,09"""

transactionDebit1 = """31.08.2023 Debit
description               -6,90"""

transactionDebit2 = """31.08.2023 Debit
description first line
description second line               -5,83"""


class ASKassenTransactionExtractor(unittest.TestCase):

    def testExtractNothingWhenNoTransaction(self):
        e = SKassenTransactionExtractor()
        transactions = e.extract(noTransaction)
        self.assertEqual(len(transactions), 0)

    def testExtractPositiveTransaction(self):
        e = SKassenTransactionExtractor()
        transactions = e.extract(statementAccount)
        self.assertEqual(transactionCredit, transactions[0])

    def testExtractNegativeTransaction(self):
        e = SKassenTransactionExtractor()
        transactions = e.extract(statementAccount)
        self.assertEqual(transactionDebit1, transactions[1])

    def testExtractLastTransactionCorrect(self):
        e = SKassenTransactionExtractor()
        transactions = e.extract(statementAccount)
        self.assertEqual(transactionDebit2, transactions[2])

    def testExtractCorrectNumberOfTransactions(self):
        e = SKassenTransactionExtractor()
        transactions = e.extract(statementAccount)
        self.assertEqual(len(transactions), 3)
