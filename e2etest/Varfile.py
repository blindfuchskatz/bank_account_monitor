SKASSE_BANK_STATEMENT_FILE = "/tmp/skasse_statement_file.pdf"
VR_BANK_STATEMENT_FILE = "/tmp/vr_bank_statement_file.csv"
SORT_RULE_FILE = "/tmp/sort_rule.csv"
CSV_OUTPUT_FILE = "/tmp/sorted_transactions.csv"
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
Mein GiroDirekt;DE1234567890;ABCDEF;VR BANK;31.08.2023;31.08.2023;Leasing Auto;DE987654321;ABCDEFGHIJ;Debit;Leasing;-310,90;EUR;1.234.567,89;;Drogeriemarkt;;DE1234556789098723;OFFLINE
Mein GiroDirekt;DE1234996790;ABCDEFGHI;VR BANK;31.08.2023;31.08.2023;Versicherung;DE987654321;ASDFGHJKLZ;Debit;Allianz;-890,83;EUR;1.234.467,89;;Grusch;;DE13456785263000123;OFFLINE
Mein GiroDirekt;DE1234996712;ABZDEFGHI;VR BANK;31.08.2023;31.08.2023;Food store;DE787654321;ASDFGHJKLY;Debit;Food;-5,83;EUR;1.234.267,89;;Auto;;DE51234567485876890000123;OFFLINE
"""
SORTED_TRANSACTION_CSV = """misc;31.08.2023;Debit;"Food";-5.83
Car;31.08.2023;Debit;"Leasing";-310.90
Insurance;31.08.2023;Debit;"Allianz";-890.83"""
ALL_MISC_TRANSACTION_CSV = """misc;31.08.2023;Debit;"Leasing";-310.90
misc;31.08.2023;Debit;"Allianz";-890.83
misc;31.08.2023;Debit;"Food";-5.83"""
EMPTY_MISC_CSV = "misc;"
HELP_TEXT = """usage: bank_account_monitor_main.py [-h] -t TRANSACTION_PATH -r SORT_RULE_PATH
                                    -o CSV_OUTPUT_FILE [-v]

options:
  -h, --help            show this help message and exit
  -t TRANSACTION_PATH, --transaction_path TRANSACTION_PATH
                        path to transaction file
  -r SORT_RULE_PATH, --sort_rule_path SORT_RULE_PATH
                        path to sort rules
  -o CSV_OUTPUT_FILE, --csv_output_file CSV_OUTPUT_FILE
                        path to csv_output_file (including file name)
  -v, --version         show program's version number and exit
"""

MISSING_BANK_STATEMENT = """usage: bank_account_monitor_main.py [-h] -t TRANSACTION_PATH -r SORT_RULE_PATH
                                    -o CSV_OUTPUT_FILE [-v]
bank_account_monitor_main.py: error: the following arguments are required: -t/--transaction_path
"""

EXCEPTION_INVALID_BANK_STATEMENT = """Account statement file does not exist:</some/path.txt>
"""
EXCEPTION_INVALID_SORT_RULE = """Cve sort rule error|invalid input path|path:</some/path.txt>
"""
EXCEPTION_INVALID_OUTPUT = """Cve presenter error|invalid input path|path:</tmp/>
"""
EXCEPTION_INVALID_OUTPUT2 = """Cve presenter error|invalid input path|path:</tmp/somefile.txt>
"""
