import unittest
from src.Sort.TransactionSorter import TransactionSorter
from src.Sort.TransactionSorter import SORT_ERROR
from src.Sort.SortRule import SortRule
from src.TransactionProvider.Transaction import Transaction
from src.Sort.TransactionSorterException import TransactionSorterException
from utest.TestHelper import CustomAssert

ta = Transaction("date1", "type1", "a", -10)
tb = Transaction("date2", "type2", "b", 60)
tab = Transaction("date3", "type3", "ab", 900)
tc = Transaction("date4", "type4", "c", 10)
td = Transaction("date5", "type5", "d", 10)
te = Transaction("date6", "type6", "e", -80)
tax = Transaction("date7", "type7", "ax", -35)
tay = Transaction("date8", "type8", "ay", -23)
taz = Transaction("date9", "type9", "az", -1000)


class ATransactionSorter(unittest.TestCase):
    def setUp(self):
        self.s = TransactionSorter()
        self.ca = CustomAssert()
        self.ca.setExceptionType(TransactionSorterException)

    def testCreateEmptyMiscDict(self):
        t_dict = self.s.sort([], [])
        self.assertListEqual(t_dict['misc'], [])

    def testSortAllToMisc(self):
        t_dict = self.s.sort([ta, tb, tab], [])
        self.assertListEqual(t_dict['misc'], [ta, tb, tab])

    def testSortByOnePattern(self):
        rules_set = [SortRule("amazon", ["b"])]

        t_dict = self.s.sort([ta, tb, tab], rules_set)

        self.assertListEqual(t_dict['misc'], [ta])
        self.assertListEqual(t_dict['amazon'], [tb, tab])

    def testSorAllToOneCategory(self):
        rules_set = [SortRule("amazon", ["b"])]

        t_dict = self.s.sort([tb, tab], rules_set)
        self.assertListEqual(t_dict["misc"], [])
        self.assertListEqual(t_dict['amazon'], [tb, tab])

    def testSortByMultiplePattern(self):
        rules_set = [SortRule("amazon", ["b", "c", "d"])]
        t = [ta, tb, tab, tc, td, te]

        t_dict = self.s.sort(t, rules_set)

        self.assertListEqual(t_dict['misc'], [ta, te])
        self.assertListEqual(t_dict['amazon'], [tb, tab, tc, td])

    def testSortMultipleCategories(self):
        r1 = SortRule("amazon", ["b", "c", "d"])
        r2 = SortRule("insurances", ["x", "y", "z"])
        rules_set = [r1, r2]
        t = [ta, tb, tab, tc, td, te, tax, tay, taz]

        t_dict = self.s.sort(t, rules_set)

        self.assertListEqual(t_dict['misc'], [ta, te])
        self.assertListEqual(t_dict['amazon'], [tb, tab, tc, td])
        self.assertListEqual(t_dict['insurances'], [tax, tay, taz])

    def testRaiseExceptionWhenTransactionAssignmentIsAmbiguous(self):
        r1 = SortRule("amazon", ["b", "c", "d"])
        r2 = SortRule("insurances", ["ab", "x", "y", "z"])
        rules_set = [r1, r2]
        t = [ta, tb, tab, tc, td, te, tax, tay, taz]

        e = SORT_ERROR.format(tab.desc, "amazon", "insurances", "b", "ab")
        self.ca.assertRaisesWithMessage(e, self.s.sort, t, rules_set)
