#!/usr/bin/env python3

from argparse import ArgumentParser
from src.Configuration.ConfigParserWrapper import ConfigParserWrapper
from src.Configuration.ConfigReader import ConfigReader
from src.Logger import Logger
from src.Presenter.PresenterFactory import PresenterFactory
from src.Sort.CsvSortRuleProvider import CsvSortRuleProvider
from src.TransactionCategorizer import TransactionCategorizer
from src.Sort.TransactionSorter import TransactionSorter
from src.TransactionProvider.TransactionProviderFactory import TransactionProviderFactory
from version import __version__


if __name__ == '__main__':

    logger = Logger()

    try:
        parser = ArgumentParser()
        parser.add_argument('-c', '--config_path',
                            help='path to config file', required=True, action='store')
        parser.add_argument('-v', '--version', action='version',
                            version='{version}'.format(version=__version__))
        arguments = parser.parse_args()

        trans_prov_factory = TransactionProviderFactory()
        pres_factory = PresenterFactory()
        config_parser = ConfigParserWrapper()
        config_reader = ConfigReader(config_parser)

        config_reader.read(arguments.config_path)

        trans_provider = trans_prov_factory.get_transaction_provider(
            config_reader.get_account_stmt_path())

        sort_rule_provider = CsvSortRuleProvider(
            config_reader.get_sort_rule_path())

        presenter = pres_factory.get(config_reader.get_presenter_config())

        sorter = TransactionSorter()

        tc = TransactionCategorizer(
            trans_provider, sort_rule_provider, sorter, presenter, logger)

        tc.run()
    except Exception as e:
        logger.error(str(e))
