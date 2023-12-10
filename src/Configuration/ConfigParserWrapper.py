
import configparser
from src.Configuration.ConfigParserInterface import ConfigParserInterface


class ConfigParserWrapper(ConfigParserInterface):
    def read(self, config_path: str) -> None:
        self.configparser = configparser.ConfigParser(interpolation=None)
        self.configparser.read(config_path)

    def get(self, section: str, option: str) -> str:
        return self.configparser.get(section=section, option=option, fallback="")

    def getboolean(self, section: str, option: str) -> bool:
        return self.configparser.getboolean(section=section,
                                            option=option,
                                            fallback=False)
