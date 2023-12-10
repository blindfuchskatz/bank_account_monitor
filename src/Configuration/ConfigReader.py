from src.Configuration.ConfigReaderException import ConfigReaderException
from src.Configuration.PresenterConfig import PresenterConfig
from src.Configuration.ConfigParserInterface import ConfigParserInterface

CONFIG_READER_ERROR = "Config file syntax error|what:{}"


class ConfigReader:
    def __init__(self, config_parser: ConfigParserInterface) -> None:
        self.config_parser = config_parser

    def read(self, config_path: str) -> None:
        try:
            self.config_parser.read(config_path)
        except Exception as e:
            raise ConfigReaderException(CONFIG_READER_ERROR.format(str(e)))

    def get_account_statement_path(self) -> str:
        return self.config_parser.get("account_statement", "input_path")

    def get_sort_rule_path(self) -> str:
        return self.config_parser.get("sort_rule", "input_path")

    def get_presenter_config(self) -> PresenterConfig:
        csv_p_enable = self.config_parser.getboolean("csv_presenter", "enable")
        csv_p_path = self.config_parser.get("csv_presenter", "output_path")

        save_p_enable = self.config_parser.getboolean(
            "savings_presenter", "enable")

        save_p_title = self.config_parser.get("savings_presenter", "title")

        save_p_ignore_list_str = self.config_parser.get(
            "savings_presenter", "ignore_categories")

        save_p_ignore_list = self.__convert_category_ignore_list(
            save_p_ignore_list_str)

        config = PresenterConfig(csv_presenter_enable=csv_p_enable,
                                 csv_output_file=csv_p_path,
                                 savings_presenter_enable=save_p_enable,
                                 title=save_p_title,
                                 ignore_list=save_p_ignore_list)

        return config

    def __convert_category_ignore_list(self, ignore_list_str):
        if ignore_list_str:
            return [item.strip() for item in ignore_list_str.split(',')]
        else:
            return []
