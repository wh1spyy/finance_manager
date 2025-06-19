# models/transaction_factory.py
from .income import Income
from .expense import Expense

class TransactionFactory:
    @staticmethod
    def create_transaction(kind: str, amount: float, category: str):
        if kind == "income":
            return Income(amount, category)
        elif kind == "expense":
            return Expense(amount, category)
        else:
            raise ValueError("Unknown transaction type")
