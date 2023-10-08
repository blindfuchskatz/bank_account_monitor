from dataclasses import dataclass
from typing import List


@dataclass
class Transaction:
    date: str
    type: str
    desc: str
    value: int


TransactionList = List[Transaction]
