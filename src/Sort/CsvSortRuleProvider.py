import re
from src.File.FileChecker import FileChecker
from src.Sort.SortRule import SortRule
from src.File.FileReader import FileReader
from src.Sort.SortRuleProvider import SortRuleProvider
from src.Sort.SortRuleProviderException import SortRuleProviderException

INVALID_LINE = "Sort rule provider error|invalid line:<{}>"
TOO_MUCH_SEARCH_PATTERN = "Sort rule provider error|too much search pattern|category:<{}>|pattern:{}"
TOO_MUCH_SORT_RULES = "Cve sort rule error|max number of sort rules exceeded|max number:{}|actual number:{}"

MAX_NUMBER_PATTERN = 100
MAX_NUMBER_SORT_RULES = 100
MIN_CSV_ENTRIES = 2

INVALID_INPUT_PATH = "Cve sort rule error|invalid input path|path:<{}>"


class CsvSortRuleProvider(SortRuleProvider):
    def __init__(self, file_checker, path) -> None:
        self.__file_checker = file_checker
        self.__path = path

        if not self.__file_checker.file_exists(self.__path):
            raise SortRuleProviderException(
                INVALID_INPUT_PATH.format(self.__path))

    def get_sort_rules(self):
        try:
            csv_lines = FileReader.get_lines(self.__path)

            if len(csv_lines) > MAX_NUMBER_SORT_RULES:
                raise SortRuleProviderException(
                    TOO_MUCH_SORT_RULES.format(MAX_NUMBER_SORT_RULES, len(csv_lines)))

            sort_rules = []
            for line in csv_lines:
                rule = self.__get_sort_rule_from_csv_line(line)
                sort_rules.append(rule)

            return sort_rules
        except Exception as e:
            raise SortRuleProviderException(e)

    def __get_sort_rule_from_csv_line(self, line):
        regex_patter = r'(?:^|;)(?:"([^"]*(?:""[^"]*)*)"|([^";]*))'

        matches = re.findall(regex_patter, line)
        csv_list = [match[0] or match[1] for match in matches]

        sort_rule = SortRule("", [])

        if self.__too_few_csv_entries(csv_list):
            raise SortRuleProviderException(INVALID_LINE.format(line))

        if self.__category_is_empty(csv_list):
            raise SortRuleProviderException(INVALID_LINE.format(line))

        sort_rule.category = csv_list[0]

        if self.__too_much_csv_entries(csv_list, ):
            raise SortRuleProviderException(
                TOO_MUCH_SEARCH_PATTERN.format(csv_list[0], len(csv_list[1:])))

        for entry in csv_list[1:]:
            if not entry:
                raise SortRuleProviderException(INVALID_LINE.format(line))
            sort_rule.pattern_list.append(entry)

        return sort_rule

    def __too_few_csv_entries(self, csv_list):
        if len(csv_list) < MIN_CSV_ENTRIES:
            return True
        return False

    def __category_is_empty(self, csv_list):
        if not csv_list[0]:
            return True
        return False

    def __too_much_csv_entries(self, csv_list):
        if len(csv_list[1:]) > MAX_NUMBER_PATTERN:
            return True
        return False
