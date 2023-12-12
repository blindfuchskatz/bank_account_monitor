import configparser
import unittest
from src.Configuration.ConfigReader import CONFIG_READER_ERROR, ConfigReader
from src.Configuration.ConfigReaderException import ConfigReaderException
from src.Configuration.PresenterConfig import CvePresConfig, PresenterId, SavingsPresConfig
from src.Configuration.ConfigParserInterface import ConfigParserInterface


NOT_FOR_TEST_RELEVANT_PATH = "/some/path"

CONFIG_CSV_PRES = """
[account_statement]
input_path = /a/b/c

[sort_rule]
input_path = /sr/p

[csv_presenter]
enable = true
output_path = /csv_p/path
"""

CONFIG_SAVE_PRES = """
[account_statement]
input_path = /a/b/c

[sort_rule]
input_path = /sr/p

[savings_presenter]
enable = true
title = savings
ignore_categories = fund, bank
"""

COMPLETE_CONFIG = """
[account_statement]
input_path = /a/b/c

[sort_rule]
input_path = /sr/p

[csv_presenter]
enable = true
output_path = /csv_p/path

[savings_presenter]
enable = true
title = savings
ignore_categories = fund, bank
"""

COMPLETE_DEFAULT_CONFIG = """
[account_statement]

[sort_rule]

[csv_presenter]
enable = true

[savings_presenter]
enable = true
"""

CONFIG_MISS_SEC_ACCOUNT_STMT = """
[sort_rule]
input_path = /sr/p
"""

CONFIG_MISS_OPTION_ACCOUNT_STMT = """
[account_statement]

[sort_rule]
input_path = /sr/p
"""

CONFIG_DISABLE_CSV_PRES = """
[csv_presenter]
enable = false
output_path = /csv_p/path
"""

CONFIG_MISS_CVE_PRES_FLAG = """
[csv_presenter]
output_path = /csv_p/path
"""

CONFIG_MISS_LIST_OPTION = """
[savings_presenter]
enable = true
title = savings
"""

CONFIG_DISABLE_SAVINGS_PRES = """
[savings_presenter]
enable = false
"""

CONFIG_MISS_SAVINGS_PRES_FLAG = """
[savings_presenter]
title = savings
"""

ERROR_NO_SECTION = """File contains no section headers.
file: '<string>', line: 1
'hello'"""


class ConfigParserStub(ConfigParserInterface):

    def inject_config(self,  config_as_str: str) -> None:
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
    def setUp(self) -> None:
        self.parser = ConfigParserStub()
        self.config_reader = ConfigReader(self.parser)

    def testReturnAccountStatementPath(self):
        self.parser.inject_config(COMPLETE_CONFIG)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(self.config_reader.get_account_stmt_path(), "/a/b/c")

    def testReturnSortRulePath(self):
        self.parser.inject_config(COMPLETE_CONFIG)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(self.config_reader.get_sort_rule_path(), "/sr/p")

    def testReturnCsvPresenterConfig(self):
        exp_c = {PresenterId.cve: CvePresConfig(csv_output_file="/csv_p/path")}
        self.parser.inject_config(CONFIG_CSV_PRES)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), exp_c)

    def testReturnNoCsvPresenterWhenDisabled(self):
        self.parser.inject_config(CONFIG_DISABLE_CSV_PRES)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), {})

    def testReturnNoCsvPresenterWhenEnableFlagMissing(self):
        self.parser.inject_config(CONFIG_MISS_CVE_PRES_FLAG)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), {})

    def testReturnSavingsPresenterConfig(self):
        pres = SavingsPresConfig(title="savings", ignore_list=["fund", "bank"])
        exp_c = {PresenterId.savings: pres}
        self.parser.inject_config(CONFIG_SAVE_PRES)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), exp_c)

    def testReturnNoSavingsPresenterWhenDisabled(self):
        self.parser.inject_config(CONFIG_DISABLE_SAVINGS_PRES)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), {})

    def testReturnNoSavingsPresenterWhenEnableFlagMissing(self):
        self.parser.inject_config(CONFIG_MISS_SAVINGS_PRES_FLAG)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), {})

    def testReturnCompletePresenterConfig(self):
        cp = CvePresConfig(csv_output_file="/csv_p/path")
        sp = SavingsPresConfig(title="savings", ignore_list=["fund", "bank"])
        exp_c = {PresenterId.cve: cp, PresenterId.savings: sp}
        self.parser.inject_config(COMPLETE_CONFIG)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertDictEqual(self.config_reader.get_presenter_config(), exp_c)

    def testReturnCompleteWithDefaultValues(self):
        cve_pres = CvePresConfig(csv_output_file="")
        save_pres = SavingsPresConfig(title="", ignore_list=[])
        exp_c = {PresenterId.cve: cve_pres, PresenterId.savings: save_pres}
        self.parser.inject_config(COMPLETE_DEFAULT_CONFIG)

        self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        self.assertEqual(self.config_reader.get_account_stmt_path(), "")
        self.assertEqual(self.config_reader.get_sort_rule_path(), "")
        self.assertDictEqual(self.config_reader.get_presenter_config(), exp_c)

    def testForwardConfigParserException(self):
        self.parser.inject_config("hello")

        try:
            self.config_reader.read(NOT_FOR_TEST_RELEVANT_PATH)

        except ConfigReaderException as e:
            self.assertEqual(
                CONFIG_READER_ERROR.format(ERROR_NO_SECTION), str(e))
