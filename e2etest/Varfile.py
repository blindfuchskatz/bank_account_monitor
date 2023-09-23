SKASSE_BANK_STATEMENT_FILE = "/tmp/skasse_statement_file.pdf"
SORT_RULE_FILE = "/tmp/sort_rule.csv"
CSV_OUTPUT_FILE = "/tmp/sorted_transactions.csv"
STDOUT_FILE = "/tmp/stdout.txt"
STDERR_FILE = "/tmp/stderr.txt"
EXAMPLE_BANK_STATEMENT = """Sirupkasse
31.08.2023 Debit
Leasing\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0-310,90
31.08.2023 Debit
Allianz\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0-890,83
31.08.2023 Debit
Food\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0-5,83
Some text"""
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

EXCEPTION_INVALID_BANK_STATEMENT = """SKassen transaction provider error|invalid input path|path:</some/path.txt>
"""
EXCEPTION_INVALID_SORT_RULE = """Cve sort rule error|invalid input path|path:</some/path.txt>
"""
EXCEPTION_INVALID_OUTPUT = """Cve presenter error|invalid input path|path:</tmp/>
"""
EXCEPTION_INVALID_OUTPUT2 = """Cve presenter error|invalid input path|path:</tmp/somefile.txt>
"""