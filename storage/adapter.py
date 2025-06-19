# storage/adapter.py
from abc import ABC, abstractmethod
from models.transaction import Transaction
from typing import List

class StorageAdapter(ABC):
    @abstractmethod
    def save(self, transactions: List[Transaction]):
        pass

    @abstractmethod
    def load(self) -> List[Transaction]:
        pass
