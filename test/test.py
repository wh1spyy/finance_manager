import unittest
import os
from datetime import datetime
from models.transaction import Transaction
from models.income import Income
from models.expense import Expense
from models.transaction_factory import TransactionFactory
from core.manager import TransactionManager
from storage.json_storage import JSONStorageAdapter
from reports.by_category import ReportByCategory
from reports.by_month import ReportByMonth
from reports.report_builder import ReportBuilder
from decorators.transaction_decorator import TransactionDecorator


class TestTransactionClasses(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_transactions.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_1_transaction_abstract_class(self):
        """Перевіряє, що Transaction є абстрактним класом"""
        with self.assertRaises(TypeError):
            Transaction(100, "Test")

    def test_2_income_creation(self):
        """Перевіряє створення доходу"""
        income = Income(1000, "Salary")
        self.assertEqual(income.type(), "Income")
        self.assertEqual(income.amount, 1000)
        self.assertEqual(income.category, "Salary")
        self.assertIsInstance(income.date, datetime)

    def test_3_expense_creation(self):
        """Перевіряє створення витрати"""
        expense = Expense(500, "Food")
        self.assertEqual(expense.type(), "Expense")
        self.assertEqual(expense.amount, 500)
        self.assertEqual(expense.category, "Food")

    def test_4_transaction_factory(self):
        """Перевіряє фабрику транзакцій"""
        income = TransactionFactory.create_transaction("income", 1000, "Salary")
        self.assertIsInstance(income, Income)

        expense = TransactionFactory.create_transaction("expense", 500, "Food")
        self.assertIsInstance(expense, Expense)

        with self.assertRaises(ValueError):
            TransactionFactory.create_transaction("invalid", 100, "Test")

    def test_5_transaction_decorator(self):
        """Перевіряє декоратор для форматування транзакцій"""
        income = Income(1000, "Salary")
        decorated = TransactionDecorator(income)
        output = decorated.display()
        self.assertIn("[INCOME]", output)
        self.assertIn("1000.00 грн", output)
        self.assertIn("Salary", output)

        expense = Expense(500, "Food")
        decorated = TransactionDecorator(expense)
        output = decorated.display()
        self.assertIn("[EXPENSE]", output)
        self.assertIn("500.00 грн", output)
        self.assertIn("Food", output)

    def test_6_storage_adapter(self):
        """Перевіряє збереження та завантаження транзакцій"""
        storage = JSONStorageAdapter(self.test_file)
        transactions = [
            Income(1000, "Salary", datetime(2023, 1, 1)),
            Expense(500, "Food", datetime(2023, 1, 2))
        ]

        storage.save(transactions)
        loaded = storage.load()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].type(), "Income")
        self.assertEqual(loaded[1].type(), "Expense")
        self.assertEqual(loaded[0].amount, 1000)
        self.assertEqual(loaded[1].amount, 500)

    def test_7_empty_storage(self):
        """Перевіряє обробку відсутності файлу зберігання"""
        storage = JSONStorageAdapter("nonexistent.json")
        transactions = storage.load()
        self.assertEqual(transactions, [])

    def test_8_transaction_manager(self):
        """Перевіряє основні операції менеджера транзакцій"""
        manager = TransactionManager(JSONStorageAdapter(self.test_file))

        # Додавання транзакцій
        manager.add_transaction(Income(1000, "Salary"))
        manager.add_transaction(Expense(500, "Food"))
        self.assertEqual(len(manager.list_transactions()), 2)

        # Видалення транзакції
        manager.remove_transaction(0)
        self.assertEqual(len(manager.list_transactions()), 1)

        # Очищення списку
        manager.clear()
        self.assertEqual(len(manager.list_transactions()), 0)

    def test_9_save_load_manager(self):
        """Перевіряє збереження та завантаження у менеджері"""
        manager = TransactionManager(JSONStorageAdapter(self.test_file))
        manager.add_transaction(Income(1000, "Salary"))
        manager.add_transaction(Expense(500, "Food"))
        manager.save()

        new_manager = TransactionManager(JSONStorageAdapter(self.test_file))
        new_manager.load()
        self.assertEqual(len(new_manager.list_transactions()), 2)

    def test_10_report_by_category(self):
        """Перевіряє звіт за категоріями"""
        transactions = [
            Income(1000, "Salary"),
            Expense(500, "Food"),
            Income(200, "Bonus"),
            Expense(300, "Food")
        ]

        report = ReportByCategory().generate(transactions)
        self.assertIn("Salary: 1000.00", report)
        self.assertIn("Food: -800.00", report)
        self.assertIn("Bonus: 200.00", report)

    def test_11_report_by_month(self):
        """Перевіряє звіт за місяцями"""
        transactions = [
            Income(1000, "Salary", datetime(2023, 1, 1)),
            Expense(500, "Food", datetime(2023, 1, 15)),
            Income(200, "Bonus", datetime(2023, 2, 1)),
            Expense(300, "Food", datetime(2023, 2, 15))
        ]

        report = ReportByMonth().generate(transactions)
        self.assertIn("2023-01: 500.00", report)
        self.assertIn("2023-02: -100.00", report)

    def test_12_report_builder(self):
        """Перевіряє побудову звіту"""
        transactions = [
            Income(1000, "Salary"),
            Expense(500, "Food")
        ]

        report = ReportBuilder() \
            .add_title("Test Report") \
            .add_body(ReportByCategory(), transactions) \
            .build()

        self.assertIn("=== Test Report ===", report)
        self.assertIn("Salary: 1000.00", report)
        self.assertIn("Food: -500.00", report)

    def test_13_negative_amount(self):
        """Перевіряє обробку негативних сум"""
        with self.assertRaises(ValueError):
            Income(-100, "Salary")

        with self.assertRaises(ValueError):
            Expense(-100, "Food")

    def test_14_empty_category(self):
        """Перевіряє обробку пустої категорії"""
        with self.assertRaises(ValueError):
            Income(100, "")

        with self.assertRaises(ValueError):
            Expense(100, "")

    def test_15_transaction_str(self):
        """Перевіряє строкове представлення транзакції"""
        income = Income(1000, "Salary", datetime(2023, 1, 1))
        self.assertEqual(str(income), "[2023-01-01] Income: 1000 (Salary)")

        expense = Expense(500, "Food", datetime(2023, 1, 2))
        self.assertEqual(str(expense), "[2023-01-02] Expense: 500 (Food)")

    def test_16_manager_remove_invalid_index(self):
        """Перевіряє обробку невірного індексу при видаленні"""
        manager = TransactionManager(JSONStorageAdapter(self.test_file))
        manager.add_transaction(Income(1000, "Salary"))

        # Не має викликати помилку при невірному індексі
        manager.remove_transaction(-1)
        manager.remove_transaction(1)
        self.assertEqual(len(manager.list_transactions()), 1)

    def test_17_report_empty_transactions(self):
        """Перевіряє звіти для пустого списку транзакцій"""
        report_category = ReportByCategory().generate([])
        self.assertIn("=== Report by Category ===", report_category)

        report_month = ReportByMonth().generate([])
        self.assertIn("=== Report by Month ===", report_month)

    def test_18_special_characters(self):
        """Перевіряє обробку спеціальних символів у категоріях"""
        manager = TransactionManager(JSONStorageAdapter(self.test_file))
        manager.add_transaction(Income(1000, "Зарплата"))
        manager.add_transaction(Expense(500, "Їжа"))
        manager.save()

        new_manager = TransactionManager(JSONStorageAdapter(self.test_file))
        new_manager.load()
        self.assertEqual(new_manager.list_transactions()[0].category, "Зарплата")
        self.assertEqual(new_manager.list_transactions()[1].category, "Їжа")

    def test_19_large_amounts(self):
        """Перевіряє обробку великих сум"""
        large_income = Income(1000000, "Big Deal")
        self.assertEqual(large_income.amount, 1000000)

        large_expense = Expense(999999.99, "Expensive")
        self.assertEqual(large_expense.amount, 999999.99)

    def test_20_date_handling(self):
        """Перевіряє обробку дат"""
        specific_date = datetime(2023, 12, 31)
        income = Income(1000, "Salary", specific_date)
        self.assertEqual(income.date, specific_date)

        # Перевірка автоматичної встановленої дати
        income_now = Income(1000, "Salary")
        self.assertAlmostEqual(
            income_now.date.timestamp(),
            datetime.now().timestamp(),
            delta=1
        )


if __name__ == "__main__":
    unittest.main()