from typing import List
from enum import Enum
from dataclasses import dataclass, field
from src.Presenter.Plotter import Plotter
from src.Presenter.PieChart import PieChart


class PresenterId(Enum):
    cve = 1
    savings = 2


@dataclass
class PresConf:
    pass


@dataclass
class CvePresConfig(PresConf):
    csv_output_file: str = ""


@dataclass
class SavingsPresConfig(PresConf):
    plotter: Plotter = PieChart()
    title: str = ""
    ignore_list: List[str] = field(default_factory=list)
