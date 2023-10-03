*** Settings ***
Library             OperatingSystem
Library             Process
Library             PdfCreator.py
Variables           Varfile.py

Test Teardown       delete test files


*** Test Cases ***
Sort skasse account statement by sort rule into csv file
    Given A skasse bank statement with three transactions
    And Two sort rules
    When Bank account monitor is called    ${SKASSE_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then A Csv file with sorted transactions where created

Sort VR bank account statement by sort rule into csv file
    [Tags]    tdd_red_phase
    Given A VR bank account statement with three transactions
    And Two sort rules
    When Bank account monitor is called    ${VR_BANK_STATEMENT_FILE}    ${SORT_RULE_FILE}    ${CSV_OUTPUT_FILE}
    Then A Csv file with sorted transactions where created

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

Some PDF file without transactions
    PdfCreator.Write    ${SKASSE_BANK_STATEMENT_FILE}    "Skassen Hello my name is Emil"

Two sort rules
    Create File    ${SORT_RULE_FILE}    Car;Leasing\nInsurance;Allianz

No Sort rule
    Create File    ${SORT_RULE_FILE}

Bank account monitor is called
    [Arguments]    ${bank_statement_file}    ${sort_rule_file}    ${output_file}

    Run Process
    ...    python3
    ...    /bank_account_monitor/bank_account_monitor_main.py
    ...    -t
    ...    ${bank_statement_file}
    ...    -r
    ...    ${sort_rule_file}
    ...    -o
    ...    ${output_file}
    ...    stdout=${STDOUT_FILE}
    ...    stderr=${STDERR_FILE}

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
    ...    -r
    ...    ${SORT_RULE_FILE}
    ...    -o
    ...    ${CSV_OUTPUT_FILE}
    ...    stderr=${STDERR_FILE}

A Csv file with sorted transactions where created
    Expect file have content    ${CSV_OUTPUT_FILE}    ${SORTED_TRANSACTION_CSV}

All Transactions are sorted to misc category
    Expect file have content    ${CSV_OUTPUT_FILE}    ${ALL_MISC_TRANSACTION_CSV}

A empty misc category is created
    Expect file have content    ${CSV_OUTPUT_FILE}    ${EMPTY_MISC_CSV}

Help text appears
    Expect file have content    ${STDOUT_FILE}    ${HELP_TEXT}

Hint to missing bank statement is appearing
    Expect file have content    ${STDERR_FILE}    ${MISSING_BANK_STATEMENT}

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
    ...    ${SKASSE_BANK_STATEMENT_FILE}
    ...    ${SORT_RULE_FILE}
    ...    ${CSV_OUTPUT_FILE}
    ...    ${STDOUT_FILE}
    ...    ${STDERR_FILE}
