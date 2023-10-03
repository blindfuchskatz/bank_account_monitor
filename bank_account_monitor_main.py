#!/usr/bin/env python3

from argparse import ArgumentParser
from src.File.FileChecker import FileChecker
from src.File.FileWriter import FileWriter
from src.Presenter.CsvPresenter import CsvPresenter
from src.Logger import Logger
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
                            help='path to transaction file', required=True, action='store')
        parser.add_argument('-r', '--sort_rule_path',
                            help='path to sort rules', required=True, action='store')
        parser.add_argument('-o', '--csv_output_file',
                            help='path to csv_output_file (including file name)', required=True, action='store')
        parser.add_argument('-v', '--version', action='version',
                            version='{version}'.format(version=__version__))
        arguments = parser.parse_args()

        file_writer = FileWriter()
        file_checker = FileChecker()
        f = TransactionProviderFactory()
        trans_provider = f.get_transaction_provider(arguments.transaction_path)
        sort_rule_provider = CsvSortRuleProvider(
            file_checker, arguments.sort_rule_path)
        sorter = TransactionSorter()
        csv_presenter = CsvPresenter(
            file_checker, file_writer, arguments.csv_output_file)

        monitor = TransactionMonitor(
            trans_provider, sort_rule_provider, sorter, csv_presenter, logger)

        monitor.monitor()
    except Exception as e:
        logger.error(str(e))
