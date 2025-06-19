# reports/by_month.py
from reports.strategy import ReportStrategy
from collections import defaultdict
from typing import List
from models.transaction import Transaction

class ReportByMonth(ReportStrategy):
    def generate(self, transactions: List[Transaction]) -> str:
        summary = defaultdict(float)
        for t in transactions:
            key = t.date.strftime("%Y-%m")
            summary[key] += t.amount if t.type() == "Income" else -t.amount

        report = "=== Report by Month ===\n"
        for month, total in sorted(summary.items()):
            report += f"{month}: {total:.2f}\n"
        return report
