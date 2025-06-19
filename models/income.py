# models/income.py
from .transaction import Transaction


class Income(Transaction):
    def __init__(self, amount: float, category: str, date=None):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        super().__init__(amount, category, date)

    def type(self) -> str:
        return "Income"