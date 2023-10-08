from src.Sort.SortRule import SortRuleList
from src.Sort.Sorted import Sorted
from src.Sort.TransactionDict import TransactionDict
from src.Sort.TransactionSorterException import TransactionSorterException
from src.TransactionProvider.Transaction import TransactionList


SORT_ERROR = "Transaction assignment ambiguous|Transaction desc:<{}>|Categories:<{},{}>|Pattern:<{},{}>"


class TransactionSorter:
    def sort(self, transactions: TransactionList, sort_rule_set: SortRuleList) -> TransactionDict:

        if sort_rule_set:
            return self.__sort(transactions, sort_rule_set)

        else:
            return {"misc": transactions}

    def __sort(self, transactions, sort_rule_set):
        transaction_dict = {"misc": []}

        for t in transactions:
            self.__sort_transaction(transaction_dict, t, sort_rule_set)

        return transaction_dict

    def __sort_transaction(self, dict, t, sort_rule_set):
        is_sorted = Sorted("", "")

        for rule in sort_rule_set:
            p = self.__get_matching_pattern(t.desc, rule.pattern_list)

            if self.__pattern_match(p):
                self.__raise_when_already_sorted(t.desc, rule, is_sorted, p)
                self.__add_to_dict(dict, rule.category, t)
                is_sorted = self.__mark_as_sorted(rule.category, p)

        if self.__transaction_was_sorted(is_sorted) == False:
            self.__add_to_dict(dict, "misc", t)

    def __get_matching_pattern(self, description, pattern_list):
        for pattern in pattern_list:
            if pattern in description:
                return pattern

        return ""

    def __pattern_match(self, pattern):
        if pattern:
            return True
        return False

    def __raise_when_already_sorted(self, description, sort_rule, is_sorted, pattern):
        if is_sorted.category != "":
            e = SORT_ERROR.format(description, is_sorted.category,
                                  sort_rule.category, is_sorted.hit_pattern, pattern)
            raise TransactionSorterException(e)

    def __add_to_dict(self, dict, category, transaction):
        if category in dict:
            dict[category].append(transaction)
        else:
            dict[category] = [transaction]

        return False

    def __mark_as_sorted(self, category, pattern):
        return Sorted(category, pattern)

    def __transaction_was_sorted(self, is_sorted):
        if is_sorted.category == "" and is_sorted.hit_pattern == "":
            return False
        return True
