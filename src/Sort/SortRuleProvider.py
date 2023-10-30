from abc import ABC, abstractmethod


class SortRuleProvider(ABC):
    @abstractmethod
    def get_sort_rules(self):
        pass  # pragma: no cover
