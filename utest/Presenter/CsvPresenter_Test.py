import unittest

from unittest.mock import MagicMock
from src.Presenter.CsvPresenter import INVALID_INPUT_PATH, NO_PATH, CsvPresenter
from src.File.FileChecker import FileChecker
from src.File.FileWriter import FileWriter
from src.Presenter.PresenterException import PresenterException
from src.TransactionProvider.Transaction import Transaction
from utest.TestHelper import CustomAssert


ta = Transaction("d1", "t1", "a", -1)
tb = Transaction("d2", "t2", "b", 2)
tc = Transaction("d3", "t3", "c", -3)

SOME_PATH = "/output/csv/path"


class ACsvPresenter(unittest.TestCase):
    def setUp(self) -> None:
        self.dir_of_file_exists = FileChecker.dir_of_file_exists
        FileChecker.dir_of_file_exists = MagicMock(return_value=True)
        self.file_writer = FileWriter()
        self.ca = CustomAssert()
        self.ca.setExceptionType(PresenterException)

    def tearDown(self) -> None:
        FileChecker.dir_of_file_exists = self.dir_of_file_exists

    def testWriteEmptyMiscDict(self):
        self.file_writer.write = MagicMock()
        cp = CsvPresenter(self.file_writer, SOME_PATH)

        cp.present({"misc": []})
        self.file_writer.write.assert_called_once_with(SOME_PATH, "misc;")

    def testWriteOneMiscDictEntry(self):
        self.file_writer.write = MagicMock()
        cp = CsvPresenter(self.file_writer, SOME_PATH)

        cp.present({"misc": [ta]})
        self.file_writer.write.assert_called_once_with(
            SOME_PATH, "misc;d1;t1;\"a\";-0.01")

    def testWriteMultiMiscDictEntries(self):
        self.file_writer.write = MagicMock()
        cp = CsvPresenter(self.file_writer, SOME_PATH)

        cp.present({"misc": [ta, tb, tc]})
        out = "misc;d1;t1;\"a\";-0.01\nmisc;d2;t2;\"b\";0.02\nmisc;d3;t3;\"c\";-0.03"
        self.file_writer.write.assert_called_once_with(SOME_PATH, out)

    def testWriteMultiCategoriesDictEntries(self):
        self.file_writer.write = MagicMock()
        cp = CsvPresenter(self.file_writer, SOME_PATH)

        cp.present({"misc": [ta, tb], "car": [tc]})
        out = "misc;d1;t1;\"a\";-0.01\nmisc;d2;t2;\"b\";0.02\ncar;d3;t3;\"c\";-0.03"
        self.file_writer.write.assert_called_once_with(SOME_PATH, out)

    def testPassPathToFileWriter(self):
        self.file_writer.write = MagicMock()
        cp = CsvPresenter(self.file_writer, SOME_PATH)

        cp.present({"misc": [ta, tb]})
        out = "misc;d1;t1;\"a\";-0.01\nmisc;d2;t2;\"b\";0.02"
        self.file_writer.write.assert_called_once_with(SOME_PATH, out)

    def testRaiseExceptionWhenOutputPathIsMissing(self):
        self.ca.assertRaisesWithMessage(
            NO_PATH, CsvPresenter, self.file_writer, "")

    def testRaiseExceptionWhenOutputPathIsInvalid(self):
        FileChecker.dir_of_file_exists = MagicMock(return_value=False)
        self.ca.assertRaisesWithMessage(
            INVALID_INPUT_PATH.format(SOME_PATH), CsvPresenter, self.file_writer, SOME_PATH)
