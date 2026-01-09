from __future__ import annotations

from pathlib import Path

from budgetbuddy.core.ledger import Ledger
from budgetbuddy.core.analytics import monthly_summary, top_categories, daily_spend_trend
from budgetbuddy.storage.json_store import JsonStore
from budgetbuddy.storage.csv_io import export_csv, import_csv


MENU = """
BudgetBuddy 💰
--------------
1) Add transaction (income/expense)
2) List transactions
3) Filter transactions
4) Update transaction
5) Delete transaction
6) Monthly summary
7) Top spending categories
8) Daily spend trend
9) Export to CSV
10) Import from CSV (replace current)
11) Save
12) Quit
"""
