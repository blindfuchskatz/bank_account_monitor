#!/usr/bin/env python3

from argparse import ArgumentParser
from src.Logger import Logger
from src.Presenter.PresenterFactory import PresenterFactory
from src.Presenter.UiConfigTranslator import UiConfigTranslator
from src.Sort.CsvSortRuleProvider import CsvSortRuleProvider
from src.TransactionMonitor import TransactionMonitor
from src.Sort.TransactionSorter import TransactionSorter
from src.TransactionProvider.TransactionProviderFactory import TransactionProviderFactory
from version import __version__


if __name__ == '__main__':

    logger = Logger()

    try:
        parser = ArgumentParser()
        parser.add_argument('-t', '--transaction_path',
                            help='path to a specific transaction file or a directory containing multiple transaction files', required=True, action='store')
        parser.add_argument('-r', '--sort_rule_path',
                            help='path to sort rules', required=True, action='store')
        parser.add_argument('-o', '--csv_output_file',
                            help='(optional) path to csv_output_file (including file name)', default="",  action='store')
        parser.add_argument('-s', '--savings', help='(optional) depict distribution of incomings and debits via pie chart',
                            default="", action='store')
        parser.add_argument('-v', '--version', action='version',
                            version='{version}'.format(version=__version__))
        arguments = parser.parse_args()

        tf = TransactionProviderFactory()
        pf = PresenterFactory()
        presenterConfig = UiConfigTranslator()
        presenterFactoryConfig = presenterConfig.translate(
            arguments.csv_output_file, arguments.savings)

        trans_provider = tf.get_transaction_provider(
            arguments.transaction_path)

        sort_rule_provider = CsvSortRuleProvider(arguments.sort_rule_path)
        sorter = TransactionSorter()

        presenter = pf.get(presenterFactoryConfig)

        monitor = TransactionMonitor(
            trans_provider, sort_rule_provider, sorter, presenter, logger)

        monitor.monitor()
    except Exception as e:
        logger.error(str(e))
