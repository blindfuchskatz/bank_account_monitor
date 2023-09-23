from dataclasses import dataclass


@dataclass
class SortRule:
    category: str
    pattern_list: list
