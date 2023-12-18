# *Bank Account Monitor*

We faced the problem that some banks do not provide appropriate or satisfactory tools to monitor or categorize transactions.
The Bank Account Monitor is a tool that reads bank account statements and categorizes the transactions using a customized sorting rule.
The maturity level or release notes are visible via the release Git tags.

## *Example Usage*

The easiest, but not resource-saving way to use the Bank Account Monitor is via the *bank_account_monitor_sdk*.
All dependencies are included in the *bank_account_monitor_sdk*. See also [Dockerfile](./docker/Dockerfile).
If you don't want the overhead caused by the SDK, feel free to create your own Python environment.
All commands below have been tested only in an Ubuntu 22.04 environment with Docker installed.

### *Building bank_account_monitor_sdk*

Enter the project root directory and execute the following command. This will build the SDK.

        ./run_build_sdk.sh

### *Start bank_account_monitor_sdk*

Enter the project root directory and execute the following command. This will start the SDK and mount the project root directory in the SDK.

        ./run_sdk.sh

### *Execute Bank Account Monitor*

To execute the Bank Account Monitor we need to place the following files in the [analyze](./analyze/) directory.

1. bank account statement file
2. sort rule file
3. configuration file

It is assumed that the bank account statement file is provided by the user. Check the release notes in the Git tags which banks are supported.

The following sections describe how to create the sort rule file, the available presentation options of the categorized transactions and how to configure the Bank Account Monitor. Finally there is a brief explanation of how to execute the Bank Account Monitor.

#### Creating a sort rule file

The Bank Account Monitor categorize the transactions in a bank account statement via sort rules.
These sort rules are put together in a sort rule csv file.
A sort rule is a csv line which have the following syntax:

        <Category;search_pattern_1;search_pattern_2;search_pattern_3>

The Bank Account Monitor goes through each transaction and checks whether any of the search patterns match a string in the transaction description.
If this is the case, the transaction is assigned to the appropriate category.

Sort rule file example:

        Car;Shell;Leasing;Gas
        Insurance;Alliance;HUK;

It is possible to create up to 100 sorting rules, each with a maximum of 100 search patterns.
Any other lines that do not conform to the syntax described above are invalid and will cause the Bank Account Monitor to abort execution. This also applies to search patterns that correspond to at least two categories.
Transactions that cannot be assigned to a category are sorted into the *misc* category.
If no sorting rule matches a transaction description, all transactions are assigned to the *misc* category.
This also happens if you pass an empty file to the Bank Account Monitor as a sorting rule file.

#### CVE Presenter

The categorized transactions can be displayed in the form of a csv file. The corresponding option is called cve presenter in the further course of the document.

The output of the csv presenter have the following syntax:

        <Category>;<Date>;<TransactionType>;<Description>;<Value>

#### Savings Presenter

There is also the possibility to present a savings calculation of the passed account statement files.
The savings are calculated by simply subtract the debits from the incomings. The distribution of savings and debits are displayed as a pie chart.
In case of a losing situation, the distribution of losings and the debits are displayed as a pie chart.
The corresponding option is called savings presenter in the further course of the document.

It is also possible to ignore certain categories when calculating savings. This is useful if, for example, you have a fund savings plan where such debits should be ignored, as in this case it is just a reallocation of your finances.

#### Creating a configuration file

All Bank Account Monitor configuration options are
explained in the table below.


| Section| Option | Description| Mandatory|
| -------- | -------- | -------- | -------- |
| account_statement | input_path | file or directory path, where the bank account statements are stored | True
|sort_rule| input_path | path to the sort rule file | True|
|csv_presenter| enable |enablement of the cve presenter. Values are true or false. If entry is missing, the default value is false| False (at least the csv presenter or the saving presenter must be active, otherwise Bank Account Monitor abort execution)|
|csv_presenter| output_path| output path where the csv file should be stored| True in case csv_presenter is enabled, otherwise False|
|savings_presenter| enable | enablement of the savings presenter. Values are true ore false. If entry is missing, the default value is false| False (at least the csv presenter or the saving presenter must be active, otherwise Bank Account Monitor abort execution)|
|savings_presenter| output_path | output path where the savings calculation as PNG image is stored|True in case savings presenter is enabled, otherwise False|
|savings_presenter|title|title of the pie chart. Is printed in the image|False|
|savings_presenter|ignore_categories| comma separated list of categories which should be ignored during the savings calculation|False|



The configuration file have the following syntax:

        [account_statement]
        input_path = <file or directory path>

        [sort_rule]
        input_path = <file path>

        [csv_presenter]
        enable = <true/false>
        output_path = <file path>

        [savings_presenter]
        enable = <true/false>
        output_path = <file path>
        title = <string>
        ignore_categories = <cat1, cat2, cat3>

#### Run the Bank Account Monitor

If the account statement file, the sorting rule file and the configuration file are available, the Bank Account Monitor can be started in the SDK as follows:

        python3 ./bank_account_monitor_main.py -c ./analyze/config.txt


In the [examples](./examples/) directory there is a example for a sort rule file,
vrbank account statement, configuration file and the corresponding sorted output as well as the savings pie chart, which are generated with the following command:

        python3 ./bank_account_monitor_main.py -c ./examples/config.txt
## *Testing*

The overall project is developed in a test-driven approach. If you want to extend the project with your own written transaction provider for a specific bank, you can use the unit and end-to-end tests of this project.

You can run the unit tests with the following command:

        ./run_utest.sh

You can run the end to end tests with the following command:

        ./run_e2etest.sh

## *Dependencies*

All dependencies of the project are listed in the Docker file. See also into the [Dockerfile](./docker/Dockerfile).

## *License*

The Bank Account Monitor is publish under this [License](./LICENSE). When you use the Bank Account Monitor in the way descried in the example above, you also shall consider the licenses of the [dependencies](#dependencies)
