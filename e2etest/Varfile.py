ANALYZE_DIR = "/tmp/analyze/"
CONFIG_FILE_PATH = ANALYZE_DIR + "config.txt"
SKASSE_BANK_STATEMENT_FILE = ANALYZE_DIR + "skasse_statement_file.pdf"
VR_BANK_STATEMENT_FILE = ANALYZE_DIR + "vr_bank_statement_file.csv"
VR_BANK_STATEMENT_FILE_WITH_SALARY = ANALYZE_DIR + "vr_bank_stmt_salary_file.csv"
SORT_RULE_FILE = ANALYZE_DIR + "sort_rule.csv"
CSV_OUTPUT_FILE = ANALYZE_DIR + "sorted_transactions.csv"
SAVINGS_OUTPUT_FILE = ANALYZE_DIR + "savings.png"
LOSIGNS_OUTPUT_FILE = ANALYZE_DIR + "losings.png"
SAVINGS_PNG = "/bank_account_monitor/e2etest/test_files/sample_savings.png"
LOSINGS_PNG = "/bank_account_monitor/e2etest/test_files/sample_losings.png"

STDOUT_FILE = "/tmp/stdout.txt"
STDERR_FILE = "/tmp/stderr.txt"
EXAMPLE_SKASSE_ACCOUNT_STATEMENT = """Sirupkasse
31.08.2023 Debit
Leasing\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0-310,90
31.08.2023 Debit
Allianz\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0-890,83
31.08.2023 Debit
Food\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0-5,83
Some text"""
EXAMPLE_VR_BANK_ACCOUNT_STATEMENT = """Bezeichnung Auftragskonto;IBAN Auftragskonto;BIC Auftragskonto;Bankname Auftragskonto;Buchungstag;Valutadatum;Name Zahlungsbeteiligter;IBAN Zahlungsbeteiligter;BIC (SWIFT-Code) Zahlungsbeteiligter;Buchungstext;Verwendungszweck;Betrag;Waehrung;Saldo nach Buchung;Bemerkung;Kategorie;Steuerrelevant;Glaeubiger ID;Mandatsreferenz
Mein GiroDirekt;DE1234567890;ABCDEF;VR BANK;01.09.2023;31.08.2023;Leasing Auto;DE987654321;ABCDEFGHIJ;Debit;Leasing;-310,90;EUR;1.234.567,89;;Drogeriemarkt;;DE1234556789098723;OFFLINE
Mein GiroDirekt;DE1234996790;ABCDEFGHI;VR BANK;01.09.2023;31.08.2023;Versicherung;DE987654321;ASDFGHJKLZ;Debit;Allianz;-890,83;EUR;1.234.467,89;;Grusch;;DE13456785263000123;OFFLINE
Mein GiroDirekt;DE1234996712;ABZDEFGHI;VR BANK;01.09.2023;31.08.2023;Food store;DE787654321;ASDFGHJKLY;Debit;Food;-5,83;EUR;1.234.267,89;;Auto;;DE51234567485876890000123;OFFLINE
"""

EXAMPLE_VR_BANK_ACCOUNT_STATEMENT_WITH_SALARY = EXAMPLE_VR_BANK_ACCOUNT_STATEMENT + """
Mein GiroDirekt;DE1234996712;ABZDEFGHI;VR BANK;01.09.2023;31.08.2023;Company xyz;DE787654321;ASDFGHJKLY;Credit;Salary;2000,11;EUR;1.234.267,89;;Auto;;DE51234567485876890000123;OFFLINE
"""
SORTED_SKASSEN_TRANS = """misc;31.08.2023;Debit;"Food";-5.83
Car;31.08.2023;Debit;"Leasing";-310.90
Insurance;31.08.2023;Debit;"Allianz";-890.83"""

SORTED_VRBANK_TRANS = """misc;01.09.2023;Debit;"Food";-5.83
Car;01.09.2023;Debit;"Leasing";-310.90
Insurance;01.09.2023;Debit;"Allianz";-890.83"""

SORTED_VRBANK_TRANS_2 = SORTED_VRBANK_TRANS + """
Incomings;01.09.2023;Credit;"Salary";2000.11"""

SORTED_SKASSEN_VRBANK_TRANS = """misc;31.08.2023;Debit;"Food";-5.83
misc;01.09.2023;Debit;"Food";-5.83
Car;31.08.2023;Debit;"Leasing";-310.90
Car;01.09.2023;Debit;"Leasing";-310.90
Insurance;31.08.2023;Debit;"Allianz";-890.83
Insurance;01.09.2023;Debit;"Allianz";-890.83"""


ALL_MISC_TRANSACTION_CSV = """misc;31.08.2023;Debit;"Leasing";-310.90
misc;31.08.2023;Debit;"Allianz";-890.83
misc;31.08.2023;Debit;"Food";-5.83"""
EMPTY_MISC_CSV = "misc;"
HELP_TEXT = """usage: bank_account_monitor_main.py [-h] -c CONFIG_PATH [-v]

options:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config_path CONFIG_PATH
                        path to config file
  -v, --version         show program's version number and exit
"""

MISSING_CONFIG_FILE = """usage: bank_account_monitor_main.py [-h] -c CONFIG_PATH [-v]
bank_account_monitor_main.py: error: the following arguments are required: -c/--config_path
"""

EXCEPTION_INVALID_BANK_STATEMENT = """Account statement file does not exist:</some/path.txt>
"""
EXCEPTION_INVALID_SORT_RULE = """Cve sort rule error|invalid input path|path:</some/path.txt>
"""
EXCEPTION_INVALID_OUTPUT = """Presenter selection error|what:<Cve presenter error|invalid input path|path:</tmp/>>
"""
EXCEPTION_INVALID_OUTPUT2 = """Cve presenter error|invalid input path|path:</tmp/somefile.txt>
"""
