from typing import List
from dataclasses import dataclass


@dataclass
class SortRule:
    category: str
    pattern_list: list


SortRuleList = List[SortRule]
