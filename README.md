# 💰 Фінансовий Менеджер — Особистий Облік Витрат

Цей проєкт — зручний інструмент для відстеження особистих фінансів з графічним інтерфейсом на Tkinter та збереженням даних у JSON.

---

# 🚀 Функціонал

* Додавання транзакцій (доходи/витрати)
* Вказівка категорій (їжа, транспорт, зарплата тощо)
* Перегляд історії транзакцій
* Генерація звітів:
  * По категоріях
  * По місяцях
* Автоматичне збереження даних
* Пошук транзакцій за категорією

---


## ✅ Тестування

Проєкт містить модульні тести для перевірки основних функцій.

### 📁 Тестові файли:

```
tests/
└── test.py
```

## ▶️ Запуск тестів:

```
pytest tests/
```

---

## 🗂️ Структура проєкту

```
expense_manager/
│
├── models/
│   ├── transaction.py         # Base клас Transaction + Factory Method
│   ├── income.py              # Income (спадкоємець Transaction)
│   ├── expense.py             # Expense (спадкоємець Transaction)
│   └── transaction_factory.py # Factory
│
├── reports/
│   ├── strategy.py            # Strategy патерн для генерації звітів
│   ├── by_category.py         # Конкретна стратегія
│   ├── by_month.py            # Конкретна стратегія
│   └── report_builder.py      # Builder
│
├── decorators/
│   └── transaction_decorator.py # Decorator для форматування
│
├── storage/
│   ├── adapter.py             # Адаптер для збереження даних
│   ├── json_storage.py        # Конкретна реалізація
│  
├── core/
│   ├── manager.py             # TransactionManager (основна логіка)
│
├── tests/
│   ├── test.py
│
├── gui.py
├── requirements.txt
└── README.md
```

---

## 📌 Використані патерни

* **Factory Method** — створення транзакцій
* **Strategy** — генерація різних типів звітів
* **Decorator** — форматування відображення транзакцій
* **Builder** — побудова складних звітів
* **Adapter** — для підтримки різних форматів збереження: JSON, CSV, SQLite.
---

## ℹ️ Автор

Студент групи ФеП-31 Гураль Олександр | 2025 | LNU