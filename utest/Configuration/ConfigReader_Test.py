import configparser
import unittest
from src.Configuration.ConfigReader import CONFIG_READER_ERROR, ConfigReader
from src.Configuration.ConfigReaderException import ConfigReaderException
from src.Configuration.PresenterConfig import PresenterConfig
from src.Configuration.ConfigParserInterface import ConfigParserInterface


NOT_FOR_TEST_RELEVANT_PATH = "/some/path"

CONFIG_CSV_PRES = """
[account_statement]
input_path = /account_statement/path

[sort_rule]
input_path = /sort_rule/path

[csv_presenter]
enable = true
output_path = /csv_presenter/path
"""

CONFIG_SAVE_PRES = """
[account_statement]
input_path = /account_statement/path

[sort_rule]
input_path = /sort_rule/path

[savings_presenter]
enable = true
title = savings
ignore_categories = fund, bank
"""

COMPLETE_CONFIG = """
[account_statement]
input_path = /account_statement/path

[sort_rule]
input_path = /sort_rule/path

[csv_presenter]
enable = true
output_path = /csv_presenter/path

[savings_presenter]
enable = false
title = savings
ignore_categories = fund, bank
"""

CONFIG_MISS_SEC_ACCOUNT_STMT = """
[sort_rule]
input_path = /sort_rule/path
"""

CONFIG_MISS_OPTION_ACCOUNT_STMT = """
[account_statement]

[sort_rule]
input_path = /sort_rule/path
"""

CONFIG_MISS_BOOL_OPTION = """
[csv_presenter]
output_path = /csv_presenter/paths
"""

CONFIG_MISS_LIST_OPTION = """
[savings_presenter]
enable = false
title = savings
"""

ERROR_NO_SECTION = """File contains no section headers.
file: '<string>', line: 1
'hello'"""


class ConfigParserStub(ConfigParserInterface):
    def __init__(self,  config_as_str: str) -> None:
        super().__init__()
        self.config_as_str = config_as_str

    def read(self, config_path: str) -> None:
        self.configparser = configparser.ConfigParser(interpolation=None)
        self.configparser.read_string(self.config_as_str)

    def get(self, section: str, option: str) -> str:
        return self.configparser.get(section=section, option=option, fallback="")

    def getboolean(self, section: str, option: str) -> bool:
        return self.configparser.getboolean(section=section,
                                            option=option,
                                            fallback=False)


class AConfigReader(unittest.TestCase):

    def testReturnAccountStatementPath(self):
        parser = ConfigParserStub(COMPLETE_CONFIG)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_account_statement_path(),
                         "/account_statement/path")

    def testReturnSortRulePath(self):
        parser = ConfigParserStub(COMPLETE_CONFIG)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_sort_rule_path(),
                         "/sort_rule/path")

    def testReturnCsvPresenterConfig(self):
        expected_conf = PresenterConfig(
            csv_presenter_enable=True,
            csv_output_file="/csv_presenter/path",
            savings_presenter_enable=False,
            title="",
            ignore_list=[])

        parser = ConfigParserStub(CONFIG_CSV_PRES)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_presenter_config(), expected_conf)

    def testReturnSavingsPresenterConfig(self):
        expected_conf = PresenterConfig(
            csv_presenter_enable=False,
            csv_output_file="",
            savings_presenter_enable=True,
            title="savings",
            ignore_list=["fund", "bank"])

        parser = ConfigParserStub(CONFIG_SAVE_PRES)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_presenter_config(), expected_conf)

    def testReturnCompletePresenterConfig(self):
        expected_conf = PresenterConfig(
            csv_presenter_enable=True,
            csv_output_file="/csv_presenter/path",
            savings_presenter_enable=False,
            title="savings",
            ignore_list=["fund", "bank"])

        parser = ConfigParserStub(COMPLETE_CONFIG)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_presenter_config(), expected_conf)

    def testEmptyStrWhenSectionMissing(self):
        parser = ConfigParserStub(CONFIG_MISS_SEC_ACCOUNT_STMT)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_account_statement_path(), "")

    def testEmptyStrWhenOptionMissing(self):
        parser = ConfigParserStub(CONFIG_MISS_OPTION_ACCOUNT_STMT)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(c.get_account_statement_path(), "")

    def testFalseWhenBoolOptionMissing(self):
        parser = ConfigParserStub(CONFIG_MISS_BOOL_OPTION)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        pres_config = c.get_presenter_config()

        self.assertEqual(pres_config.csv_presenter_enable, False)

    def testEmptyListWhenListOptionMissing(self):
        parser = ConfigParserStub(CONFIG_MISS_LIST_OPTION)
        c = ConfigReader(parser)

        c.read(NOT_FOR_TEST_RELEVANT_PATH)

        pres_config = c.get_presenter_config()

        self.assertEqual(pres_config.ignore_list, [])

    def testForwardConfigParserException(self):
        parser = ConfigParserStub("hello")
        c = ConfigReader(parser)

        try:
            c.read(NOT_FOR_TEST_RELEVANT_PATH)

        except ConfigReaderException as e:
            self.assertEqual(
                CONFIG_READER_ERROR.format(ERROR_NO_SECTION), str(e))
