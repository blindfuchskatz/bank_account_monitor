from abc import abstractmethod
from typing import Dict


class Plotter:
    @abstractmethod
    def plot(self, title: str, data_dict: Dict):
        pass
