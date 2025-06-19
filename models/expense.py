# models/expense.py
from .transaction import Transaction


class Expense(Transaction):
    def __init__(self, amount: float, category: str, date=None):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        super().__init__(amount, category, date)

    def type(self) -> str:
        return "Expense"