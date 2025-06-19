# storage/json_storage.py
import json
from typing import List
from models.transaction import Transaction
from models.income import Income
from models.expense import Expense
from storage.adapter import StorageAdapter
from datetime import datetime

class JSONStorageAdapter(StorageAdapter):
    def __init__(self, filepath="transactions.json"):
        self.filepath = filepath

    def save(self, transactions: List[Transaction]):
        data = [
            {
                "type": t.type(),
                "amount": t.amount,
                "category": t.category,
                "date": t.date.isoformat()
            }
            for t in transactions
        ]
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load(self) -> List[Transaction]:
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                result = []
                for item in data:
                    date = datetime.fromisoformat(item["date"])
                    if item["type"] == "Income":
                        result.append(Income(item["amount"], item["category"], date))
                    elif item["type"] == "Expense":
                        result.append(Expense(item["amount"], item["category"], date))
                return result
        except FileNotFoundError:
            return []
