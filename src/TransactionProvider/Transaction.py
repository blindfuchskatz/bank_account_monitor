from dataclasses import dataclass


@dataclass
class Transaction:
    date: str
    type: str
    desc: str
    value: int
