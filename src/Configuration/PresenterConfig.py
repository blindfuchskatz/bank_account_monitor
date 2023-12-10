from typing import List
from dataclasses import dataclass, field
from src.Presenter.Plotter import Plotter
from src.Presenter.PieChart import PieChart


@dataclass
class PresenterConfig:
    csv_presenter_enable: bool = False
    csv_output_file: str = ""

    savings_presenter_enable: bool = False
    plotter: Plotter = PieChart()
    title: str = ""
    ignore_list: List[str] = field(default_factory=list)
