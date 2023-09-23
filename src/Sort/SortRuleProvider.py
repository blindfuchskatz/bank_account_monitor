from abc import abstractmethod


class SortRuleProvider:
    @abstractmethod
    def get_sort_rules(self):
        pass
