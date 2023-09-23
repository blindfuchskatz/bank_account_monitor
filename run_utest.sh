#!/bin/bash

coverage run -m --source=/bank_account_monitor/ utest.Unit_Test
coverage html -d /bank_account_monitor/utest/coverage_report/
rm /bank_account_monitor/.coverage
mypy ./


html_file="/bank_account_monitor/utest/coverage_report/index.html"
coverage_percentage=$(grep -oP '<span class="pc_cov">\K[^<]+' "$html_file")
echo -e "\033[1;32mUnit test coverage percentage: $coverage_percentage\033[0m"