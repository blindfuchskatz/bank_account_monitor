import unittest
from utest.TransactionProvider.SKassen.SKassenTransactionExtractor_Test import ASKassenTransactionExtractor
from utest.TransactionProvider.SKassen.SKassenTransactionConverter_Test import ASKassenTransactionConverter
from utest.TransactionProvider.VrBank.VrBankTransactionConverter_Test import AVrBankTransactionConverter
from utest.TransactionProvider.VrBank.VrBankTransactionProvider_Test import AVrBankTransactionProvider
from utest.TransactionProvider.MultiTransactionProvider_Test import AMultiTransactionProvider
from utest.TransactionProvider.TransactionProviderFactory_Test import ATransactionProviderFactory
from utest.Sort.TransactionSorter_Test import ATransactionSorter
from utest.TransactionProvider.SKassen.SKassenTransactionProvider_Test import ASKassenTransactionProvider
from utest.Sort.CsvSortRuleProvider_Test import ACsvSortRuleProvider
from utest.File.FileReader_Test import AFileReader
from utest.TransactionMonitor_Test import ATransactionMonitor
from utest.Presenter.CsvPresenter_Test import ACsvPresenter
from utest.Presenter.SavingsPresenter_Test import ASavingsPresenter
from utest.Presenter.PresenterFactory_Test import APresenterFactory
from utest.Presenter.UiConfigTranslator_Test import AUiConfigTranslator
if __name__ == '__main__':
    unittest.main()
