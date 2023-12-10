from abc import ABC, abstractmethod


class ConfigParserInterface(ABC):
    @abstractmethod
    def read(self, config_path: str) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def get(self, section: str, option: str) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def getboolean(self, section: str, option: str) -> bool:
        pass  # pragma: no cover
