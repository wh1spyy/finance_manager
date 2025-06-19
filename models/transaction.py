# models/transaction.py
from abc import ABC, abstractmethod
from datetime import datetime

class Transaction(ABC):
    def __init__(self, amount: float, category: str, date: datetime = None):
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        self.amount = amount
        self.category = category.strip()
        self.date = date or datetime.now()

    @abstractmethod
    def type(self) -> str:
        pass

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d')}] {self.type()}: {self.amount} ({self.category})"