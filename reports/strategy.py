# reports/strategy.py
from abc import ABC, abstractmethod
from models.transaction import Transaction
from typing import List

class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, transactions: List[Transaction]) -> str:
        pass
