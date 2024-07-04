
import configparser
from src.File.FileChecker import FileChecker
from src.Configuration.ConfigParserInterface import ConfigParserInterface

CONFIG_FILE_DOES_NOT_EXIST = "<{}> does not exist"


class ConfigParserException(Exception):
    """Raised on sort rule provider error"""


class ConfigParserWrapper(ConfigParserInterface):
    def read(self, config_path: str) -> None:
        if FileChecker.file_exists(config_path) == False:
            raise ConfigParserException(
                CONFIG_FILE_DOES_NOT_EXIST.format(config_path))
        self.configparser = configparser.ConfigParser(interpolation=None)
        self.configparser.read(config_path)

    def get(self, section: str, option: str) -> str:
        return self.configparser.get(section=section, option=option, fallback="")

    def getboolean(self, section: str, option: str) -> bool:
        return self.configparser.getboolean(section=section,
                                            option=option,
                                            fallback=False)
