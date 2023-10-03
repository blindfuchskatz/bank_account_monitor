from typing import List
from src.File.FileChecker import FileChecker
from src.File.FileReader import FileReader
from src.TransactionProvider.Transaction import Transaction
from src.TransactionProvider.TransactionProvider import TransactionProvider
from src.TransactionProvider.TransactionProviderException import TransactionProviderException
from src.TransactionProvider.VrBank.VrBankTransactionConverter import VrBankTransactionConverter


PROVIDER_EXCEPTION = "VR bank transaction provider error|what:<{}>"
HEAD_LINE = """Bezeichnung Auftragskonto;IBAN Auftragskonto;BIC Auftragskonto;Bankname Auftragskonto;Buchungstag;Valutadatum;Name Zahlungsbeteiligter;IBAN Zahlungsbeteiligter;BIC (SWIFT-Code) Zahlungsbeteiligter;Buchungstext;Verwendungszweck;Betrag;Waehrung;Saldo nach Buchung;Bemerkung;Kategorie;Steuerrelevant;Glaeubiger ID;Mandatsreferenz"""
IS_NOT_ACCOUNT_STATEMENT = "no vr bank account statement"


class VrBankTransactionProvider(TransactionProvider):
    def __init__(self, file_checker: FileChecker, path: str) -> None:
        super().__init__(file_checker, path, "VR bank")
        if not self.is_account_statement():
            raise TransactionProviderException(PROVIDER_EXCEPTION.format(
                IS_NOT_ACCOUNT_STATEMENT))

    def get_transactions(self) -> List[Transaction]:
        try:
            csv_line_list = FileReader.get_lines(self._path)
            t_list = []
            c = VrBankTransactionConverter()

            for csv_line in csv_line_list[1:]:
                t_list.append(c.convert(csv_line))

            return t_list
        except Exception as e:
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(str(e)))

    def is_account_statement(self) -> bool:
        try:
            csv_line_list = FileReader.get_lines(self._path)
            if not csv_line_list:
                return False

            if csv_line_list[0] == HEAD_LINE:
                return True
            return False
        except Exception as e:
            raise TransactionProviderException(
                PROVIDER_EXCEPTION.format(str(e)))
