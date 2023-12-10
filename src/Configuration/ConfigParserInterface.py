from abc import ABC, abstractmethod


class ConfigParserInterface(ABC):
    @abstractmethod
    def read(self, config_path: str) -> None:
        pass

    @abstractmethod
    def get(self, section: str, option: str) -> str:
        pass

    @abstractmethod
    def getboolean(self, section: str, option: str) -> bool:
        pass
