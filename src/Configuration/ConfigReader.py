from typing import Dict
from src.Configuration.ConfigReaderException import ConfigReaderException
from src.Configuration.PresenterConfig import CvePresConfig, PresConf, PresenterId, SavingsPresConfig
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

    def get_account_stmt_path(self) -> str:
        return self.config_parser.get("account_statement", "input_path")

    def get_sort_rule_path(self) -> str:
        return self.config_parser.get("sort_rule", "input_path")

    def get_presenter_config(self) -> Dict[PresenterId, PresConf]:
        pres_conf_dict: Dict[PresenterId, PresConf] = {}
        pres_conf_dict = self.__get_cve_pres_conf(pres_conf_dict)
        pres_conf_dict = self.__get_save_pres_conf(pres_conf_dict)

        return pres_conf_dict

    def __get_cve_pres_conf(self, conf_dict):
        enable = self.config_parser.getboolean("csv_presenter", "enable")
        csv_p_path = self.config_parser.get("csv_presenter", "output_path")

        if not enable:
            return conf_dict

        conf_dict[PresenterId.cve] = CvePresConfig(csv_output_file=csv_p_path)

        return conf_dict

    def __get_save_pres_conf(self, conf_dict):
        enable = self.config_parser.getboolean("savings_presenter", "enable")
        plot_path = self.config_parser.get("savings_presenter", "output_path")
        title = self.config_parser.get("savings_presenter", "title")
        il = self.config_parser.get("savings_presenter", "ignore_categories")

        ignore_list = self.__convert_category_ignore_list(il)

        if not enable:
            return conf_dict

        pres = SavingsPresConfig(plot_output_file=plot_path,
                                 title=title,
                                 ignore_list=ignore_list)

        conf_dict[PresenterId.savings] = pres

        return conf_dict

    def __convert_category_ignore_list(self, ignore_list_str):
        if ignore_list_str:
            return [item.strip() for item in ignore_list_str.split(',')]
        else:
            return []
