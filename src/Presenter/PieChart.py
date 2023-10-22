from typing import Dict
from matplotlib import pyplot as plt

from src.Presenter.Plotter import Plotter


class PieChart(Plotter):
    def plot(self, title: str, data_dict: Dict) -> None:

        labels = list(data_dict.keys())
        sizes = list(data_dict.values())

        plt.figure(figsize=(10, 10))
        plt.pie(sizes, labels=labels,
                autopct=lambda p: f'{p * sum(sizes) / 10000:.2f}', startangle=90)
        plt.axis('equal')
        plt.title(title)
        plt.show()
