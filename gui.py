# gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from models.transaction_factory import TransactionFactory
from core.manager import TransactionManager
from storage.json_storage import JSONStorageAdapter
from reports.report_builder import ReportBuilder
from reports.by_category import ReportByCategory
from reports.by_month import ReportByMonth
from decorators.transaction_decorator import TransactionDecorator

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Фінансовий Менеджер 💰")
        self.manager = TransactionManager(JSONStorageAdapter())
        self.manager.load()

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        self.add_buttons()
        self.output = tk.Text(self.frame, height=20, width=60)
        self.output.pack()

    def add_buttons(self):
        tk.Button(self.frame, text="➕ Додати транзакцію", command=self.add_transaction).pack(fill="x")
        tk.Button(self.frame, text="📄 Переглянути транзакції", command=self.show_transactions).pack(fill="x")
        tk.Button(self.frame, text="📊 Звіт по категоріях", command=self.report_by_category).pack(fill="x")
        tk.Button(self.frame, text="📅 Звіт по місяцях", command=self.report_by_month).pack(fill="x")
        tk.Button(self.frame, text="💾 Зберегти", command=self.save).pack(fill="x")
        tk.Button(self.frame, text="🚪 Вийти", command=self.root.quit).pack(fill="x")

    def add_transaction(self):
        t_type = simpledialog.askstring("Тип", "income або expense?")
        if t_type not in ["income", "expense"]:
            messagebox.showerror("Помилка", "Невірний тип")
            return
        amount = simpledialog.askfloat("Сума", "Введіть суму:")
        category = simpledialog.askstring("Категорія", "Введіть категорію:")
        t = TransactionFactory.create_transaction(t_type, amount, category)
        self.manager.add_transaction(t)
        messagebox.showinfo("Успіх", "Транзакція додана!")

    def show_transactions(self):
        self.output.delete(1.0, tk.END)
        for t in self.manager.list_transactions():
            self.output.insert(tk.END, TransactionDecorator(t).display() + "\n")

    def report_by_category(self):
        report = ReportBuilder()\
            .add_title("Звіт по категоріях")\
            .add_body(ReportByCategory(), self.manager.list_transactions())\
            .build()
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, report)

    def report_by_month(self):
        report = ReportBuilder()\
            .add_title("Звіт по місяцях")\
            .add_body(ReportByMonth(), self.manager.list_transactions())\
            .build()
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, report)

    def save(self):
        self.manager.save()
        messagebox.showinfo("Збережено", "Дані успішно збережено!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
