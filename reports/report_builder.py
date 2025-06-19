# reports/report_builder.py
from reports.strategy import ReportStrategy
from models.transaction import Transaction
from typing import List

class ReportBuilder:
    def __init__(self):
        self.title = ""
        self.body = ""

    def add_title(self, title: str):
        self.title = f"=== {title} ===\n"
        return self

    def add_body(self, strategy: ReportStrategy, transactions: List[Transaction]):
        self.body = strategy.generate(transactions)
        return self

    def build(self) -> str:
        return self.title + self.body
