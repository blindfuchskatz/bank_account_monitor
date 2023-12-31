from abc import ABC, abstractmethod
from typing import Dict


class Plotter(ABC):
    @abstractmethod
    def plot(self, title: str, data_dict: Dict[str, int], path: str) -> None:
        pass  # pragma: no cover
