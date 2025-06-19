# core/manager.py
from models.transaction import Transaction
from storage.adapter import StorageAdapter
from reports.strategy import ReportStrategy
from typing import List

class TransactionManager:
    def __init__(self, storage: StorageAdapter):
        self.transactions: List[Transaction] = []
        self.storage = storage

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def remove_transaction(self, index: int):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]

    def save(self):
        self.storage.save(self.transactions)

    def load(self):
        self.transactions = self.storage.load()

    def generate_report(self, strategy: ReportStrategy) -> str:
        return strategy.generate(self.transactions)

    def list_transactions(self):
        return self.transactions

    def clear(self):
        self.transactions = []