import re


class SKassenTransactionExtractor:
    def extract(self, raw_pdf_text):
        transaction_pattern = r"(\d{2}\.\d{2}\.\d{4} [^\n]*\n[\s\S]*? {4,}-?.+,\d{2})\n"
        matches = re.findall(transaction_pattern, raw_pdf_text)

        transactions = []

        for match in matches:
            transactions.append(match)

        return transactions
