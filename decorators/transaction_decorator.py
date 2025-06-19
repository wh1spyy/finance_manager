class TransactionDecorator:
    def __init__(self, transaction):
        self.transaction = transaction

    def display(self):
        date_str = self.transaction.date.strftime("%Y-%m-%d")
        t_type = "INCOME" if self.transaction.__class__.__name__ == "Income" else "EXPENSE"
        return f"[{t_type}] {self.transaction.amount:.2f} грн - {self.transaction.category} ({date_str})"
