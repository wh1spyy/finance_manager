# reports/by_category.py
from reports.strategy import ReportStrategy
from collections import defaultdict
from typing import List
from models.transaction import Transaction


class ReportByCategory(ReportStrategy):
    def generate(self, transactions: List[Transaction]) -> str:
        summary = defaultdict(float)
        for t in transactions:
            summary[t.category] += t.amount if t.type() == "Income" else -t.amount

        report = "=== Report by Category ===\n"
        for category, total in summary.items():
            report += f"{category}: {total:.2f}\n"
        return report
