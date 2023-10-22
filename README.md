# *Bank Account Monitor*

We faced the problem that some banks do not provide appropriate or satisfactory tools to monitor or categorize transactions.
The Bank Account Monitor is a tool that reads bank statements and categorizes the transactions using a customized sorting rule.
The maturity level or release notes are visible via the release Git tags.

## *Example Usage*

The easiest, but not resource-saving way to use the Bank Account Monitor is via the *bank_account_monitor_sdk*.
All dependencies are included in the *bank_account_monitor_sdk*. See also into the [Dockerfile](./docker/Dockerfile).
If you don't want the overhead caused by the SDK, feel free to create your own Python environment.
All commands below have been tested only in an Ubuntu 22.04 environment with Rootless Docker installed

### *Building bank_account_monitor_sdk*

Enter the project root directory and execute the following command. This will build the SDK.

        ./run_build_sdk.sh

### *Start bank_account_monitor_sdk*

Enter the project root directory and execute the following command. This will start the SDK and mount the project root directory into the SDK.

        ./run_sdk.sh

### *Execute Bank Account Monitor*

First, you need to place a bank statement file in the [analyze](./analyze/) directory.
Next, you need to create a sorting rules file and also place it in the [analyze](./analyze/) directory.

#### Creating a sort rule file

The Bank Account Monitor categorize the transactions in a bank account statement via sort rules.
These sort rules are put together in a sort rule csv file.
A sort rule is a csv line which have the following syntax:

        <Category;search_pattern_1;search_pattern_2;search_pattern_3>

The Bank Account Monitor goes through each transaction and checks whether any of the search patterns match a string in the transaction description.
If this is the case, the transaction is assigned to the appropriate category.

Example:

        Car;Shell;Leasing;Gas
        Insurance;Alliance;HUK;

It is possible to create up to 100 sorting rules, each with a maximum of 100 search patterns.
Any other lines that do not conform to the syntax described above are invalid and will cause the Bank Account Monitor to abort execution. This also applies to search patterns that correspond to at least two categories.
Transactions that cannot be assigned to a category are sorted into the *misc* category.
If no sorting rule matches a transaction description, all transactions are assigned to the *misc* category.
This also happens if you pass an empty file to the Bank Account Monitor as a sorting rule file.

If the account statement and the sorting rule file are available, the Bank Account Monitor can be started in the SDK as follows:

        python3 ./bank_account_monitor_main.py \
        -t ./analyze/bank_account_statement_file \
        -r ./analyze/sort_rule_file \
        -o ./analyze/output_file

The output file contain the sorted transactions in a CSV syntax.
The Syntax is as follows:

        <Category>;<Date>;<TransactionType>;<Description>;<Value>

It is also possible to let the Bank Account Monitor plot a savings distribution of the incomings and debits of the account statement as pie chart.
We can achieve this by calling the Bank Account Monitor as follows:

        python3 ./bank_account_monitor_main.py \
        -t ./analyze/bank_account_statement_file \
        -r ./analyze/sort_rule_file \
        -o ./analyze/output_file
        -s <title;category1;category2>

The *-o* parameter is optional in that case.
The CSV string passed by the parameter *-s*, contains the title of the pie chart as well as a list of categories which shall be ignored.
This is useful when you have for instance a fund savings plan where this kinds of debits should be ignored, because in that case those debits are only a balancing of your finances. It is possible to pass only the title without ignore list.

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
