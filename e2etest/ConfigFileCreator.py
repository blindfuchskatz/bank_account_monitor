CONFIG_TEMPLATE = """
[account_statement]
input_path = {}

[sort_rule]
input_path = {}

[csv_presenter]
enable = {}
output_path = {}

[savings_presenter]
enable = {}
output_path = {}
title = savings
ignore_categories = fund, bank
"""


class ConfigFileCreator:
    def create(self, config_path: str,
               account_stmt_path: str,
               sort_rule_path: str,
               csv_pres_enable: bool,
               csv_output_path: str,
               save_pres_enable: bool,
               save_output_path: str):

        content = CONFIG_TEMPLATE.format(account_stmt_path,
                                         sort_rule_path,
                                         csv_pres_enable,
                                         csv_output_path,
                                         save_pres_enable,
                                         save_output_path)

        f = open(config_path, 'w')
        f.write(content)
        f.close()
