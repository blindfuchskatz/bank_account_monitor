*** Settings ***
Library             OperatingSystem
Library             Process
Library             PdfCreator.py
Library             ConfigFileCreator.py
Variables           Varfile.py

Test Setup          Create Directory    ${ANALYZE_DIR}
Test Teardown       delete test files


*** Test Cases ***
Sort skasse account statement by sort rule into csv file
    Given A skasse bank statement with three transactions
    And Two sort rules
    When Bank account monitor is called    ${SKASSE_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then A Csv file with sorted transactions where created    ${SORTED_SKASSEN_TRANS}

Sort VR bank account statement by sort rule into csv file
    Given A VR bank account statement with three transactions
    And Two sort rules
    When Bank account monitor is called    ${VR_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then A Csv file with sorted transactions where created    ${SORTED_VRBANK_TRANS}

Sort all skassen and vr bank transactions within a directory
    Given A skasse bank statement with three transactions
    And A VR bank account statement with three transactions
    And Two sort rules
    And Some other file
    When Bank account monitor is called    ${ANALYZE_DIR}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then A Csv file with sorted transactions where created    ${SORTED_SKASSEN_VRBANK_TRANS}

Sort all transaction to misc when sort rule file is empty
    Given A skasse bank statement with three transactions
    And No Sort rule
    When Bank account monitor is called    ${SKASSE_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then All Transactions are sorted to misc category

Creaty empty misc output when no transaction available
    Given Some PDF file without transactions
    And No Sort rule
    When Bank account monitor is called    ${SKASSE_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then A empty misc category is created

Store calculated asset savings as pie chart in png image
    Given A VR bank account statement with three debits and one credit
    And Two sort rules
    When Bank account monitor is called to present savings
    Then Savings are stored

Store calculated asset losings as pie chart in png image
    Given A VR bank account statement with three transactions
    And Two sort rules
    When Bank account monitor is called to present losings
    Then Losings are stored

Sort VR bank account statement into csv file and show savings
    Given A VR bank account statement with three debits and one credit
    And Three sort rules
    When Bank account monitor is called to present sorted transactions and savings
    Then A Csv file with sorted transactions where created    ${SORTED_VRBANK_TRANS_2}
    And Savings are stored

Show complete help text
    When Bank account monitor help is called
    Then Help text appears

Show help when one of the mandatory input parameter is missing
    When Bank account monitor is called without bank statement
    Then Hint to missing bank statement is appearing

Exception for invalid bank statement file is logged
    When Bank account monitor is called    /some/path.txt    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then Error is logged to standard err    ${EXCEPTION_INVALID_BANK_STATEMENT}

Exception for invalid sort rule file is logged
    Given A skasse bank statement with three transactions
    When Bank account monitor is called    ${SKASSE_BANK_STATEMENT_FILE}    /some/path.txt    ${CSV_OUTPUT_FILE}
    Then Error is logged to standard err    ${EXCEPTION_INVALID_SORT_RULE}

Exception for passing only directory of output file is logged
    Given A skasse bank statement with three transactions
    And Two sort rules
    When Bank account monitor is called    ${SKASSE_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    /tmp/
    Then Error is logged to standard err    ${EXCEPTION_INVALID_OUTPUT}


*** Keywords ***
A skasse bank statement with three transactions
    PdfCreator.Write    ${SKASSE_BANK_STATEMENT_FILE}    ${EXAMPLE_SKASSE_ACCOUNT_STATEMENT}

A VR bank account statement with three transactions
    Create File    ${VR_BANK_STATEMENT_FILE}    ${EXAMPLE_VR_BANK_ACCOUNT_STATEMENT}

A VR bank account statement with three debits and one credit
    Create File    ${VR_BANK_STATEMENT_FILE_WITH_SALARY}
    ...    ${EXAMPLE_VR_BANK_ACCOUNT_STATEMENT_WITH_SALARY}

Some PDF file without transactions
    PdfCreator.Write    ${SKASSE_BANK_STATEMENT_FILE}    "Skassen Hello my name is Emil"

Two sort rules
    Create File    ${SORT_RULE_FILE}    Car;Leasing\nInsurance;Allianz

Three sort rules
    Create File    ${SORT_RULE_FILE}    Car;Leasing\nInsurance;Allianz\nIncomings;Salary

No Sort rule
    Create File    ${SORT_RULE_FILE}

Some other file
    Copy File    ./e2etest/test_files/ods_data.ods    ${ANALYZE_DIR}

Generic bank account monitor called
    [Arguments]    ${bank_statement_file}
    ...    ${sort_rule_file}
    ...    ${enable_csv_pres}
    ...    ${csv_pres_out}
    ...    ${enable_savings_pres}
    ...    ${savings_pres_out}

    ConfigFileCreator.Create
    ...    ${CONFIG_FILE_PATH}
    ...    ${bank_statement_file}
    ...    ${sort_rule_file}
    ...    ${enable_csv_pres}
    ...    ${csv_pres_out}
    ...    ${enable_savings_pres}
    ...    ${savings_pres_out}

    Run Process
    ...    python3
    ...    /bank_account_monitor/bank_account_monitor_main.py
    ...    -c
    ...    ${CONFIG_FILE_PATH}
    ...    stdout=${STDOUT_FILE}
    ...    stderr=${STDERR_FILE}

Bank account monitor is called
    [Arguments]    ${bank_statement_file}    ${sort_rule_file}    ${output_file}
    Generic bank account monitor called
    ...    ${bank_statement_file}
    ...    ${sort_rule_file}
    ...    ${True}
    ...    ${output_file}
    ...    ${False}
    ...    /some/path

Bank account monitor is called to present sorted transactions and savings
    Generic bank account monitor called
    ...    ${VR_BANK_STATEMENT_FILE_WITH_SALARY}
    ...    ${SORT_RULE_FILE}
    ...    ${True}
    ...    ${CSV_OUTPUT_FILE}
    ...    ${True}
    ...    ${SAVINGS_OUTPUT_FILE}

Bank account monitor is called to present savings
    Bank account monitor is called to present account statement
    ...    ${VR_BANK_STATEMENT_FILE_WITH_SALARY}
    ...    ${SORT_RULE_FILE}
    ...    ${SAVINGS_OUTPUT_FILE}

Bank account monitor is called to present losings
    Bank account monitor is called to present account statement
    ...    ${VR_BANK_STATEMENT_FILE}
    ...    ${SORT_RULE_FILE}
    ...    ${LOSIGNS_OUTPUT_FILE}

Bank account monitor is called to present account statement
    [Arguments]    ${bank_statement_file}    ${sort_rule_file}    ${output_file}
    Generic bank account monitor called
    ...    ${bank_statement_file}
    ...    ${sort_rule_file}
    ...    ${False}
    ...    /some/path
    ...    ${True}
    ...    ${output_file}

Bank account monitor help is called
    Run Process
    ...    python3
    ...    /bank_account_monitor/bank_account_monitor_main.py
    ...    -h
    ...    stdout=${STDOUT_FILE}

Bank account monitor is called without bank statement
    Run Process
    ...    python3
    ...    /bank_account_monitor/bank_account_monitor_main.py
    ...    stderr=${STDERR_FILE}

A Csv file with sorted transactions where created
    [Arguments]    ${sorted_transactions_csv}
    Expect file have content    ${CSV_OUTPUT_FILE}    ${sorted_transactions_csv}
    Expect file have content    ${STDOUT_FILE}    ${EMPTY}
    Expect file have content    ${STDERR_FILE}    ${EMPTY}

Savings are stored
    ${result}    Evaluate    filecmp.cmp('${SAVINGS_OUTPUT_FILE}', '${SAVINGS_PNG}')
    Should Be True    ${result}

Losings are stored
    ${result}    Evaluate    filecmp.cmp('${LOSIGNS_OUTPUT_FILE}', '${LOSINGS_PNG}')
    Should Be True    ${result}

All Transactions are sorted to misc category
    Expect file have content    ${CSV_OUTPUT_FILE}    ${ALL_MISC_TRANSACTION_CSV}

A empty misc category is created
    Expect file have content    ${CSV_OUTPUT_FILE}    ${EMPTY_MISC_CSV}

Help text appears
    Expect file have content    ${STDOUT_FILE}    ${HELP_TEXT}

Hint to missing bank statement is appearing
    Expect file have content    ${STDERR_FILE}    ${MISSING_CONFIG_FILE}

Error is logged to standard err
    [Arguments]    ${exception_msg}
    Expect file have content    ${STDERR_FILE}    ${exception_msg}

Expect file have content
    [Arguments]    ${file}    ${expected_msg}
    File Should Exist    ${file}
    ${content}    Get File    ${file}
    Should Be Equal As Strings    ${content}    ${expected_msg}

delete test files
    Remove Files
    ...    ${STDOUT_FILE}
    ...    ${STDERR_FILE}
    Remove Directory    ${ANALYZE_DIR}    True
