from typing import List
from src.Presenter.PieChart import PieChart
from src.Presenter.Plotter import Plotter
from dataclasses import dataclass, field


@dataclass
class PresenterFactoryConfig:
    csv_output_file: str = ""
    plotter: Plotter = PieChart()
    title: str = ""
    ignore_list: List[str] = field(default_factory=list)
