from src.Logger import Logger
from src.Presenter.TransactionPresenter import TransactionPresenter
from src.Sort.SortRuleProvider import SortRuleProvider
from src.Sort.TransactionSorter import TransactionSorter
from src.TransactionProvider.TransactionProvider import TransactionProvider


class TransactionMonitor:
    def __init__(self, t_provider: TransactionProvider, r_provider: SortRuleProvider, t_sorter: TransactionSorter, t_presenter: TransactionPresenter, logger: Logger) -> None:
        self.__t_provider = t_provider
        self.__r_provider = r_provider
        self.__t_sorter = t_sorter
        self.__t_presenter = t_presenter
        self.__logger = logger

    def monitor(self) -> None:
        try:
            transaction_list = self.__t_provider.get_transactions()
            sort_rule_list = self.__r_provider.get_sort_rules()

            t_dict = self.__t_sorter.sort(transaction_list, sort_rule_list)

            self.__t_presenter.present(t_dict)
        except Exception as e:
            self.__logger.error(str(e))
