CONFIG_TEMPLATE = """
[account_statement]
input_path = {}

[sort_rule]
input_path = {}

[csv_presenter]
enable = true
output_path = {}
"""


class ConfigFileCreator:
    def create(self, config_path: str,
               account_stmt_path: str,
               sort_rule_path: str,
               csv_output_path: str):

        content = CONFIG_TEMPLATE.format(account_stmt_path,
                                         sort_rule_path,
                                         csv_output_path)

        f = open(config_path, 'w')
        f.write(content)
        f.close()
