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


def _prompt(msg: str) -> str:
    return input(msg).strip()


def _print_tx(t) -> None:
    print(f"{t.id} | {t.tx_date} | {t.tx_type:<7} | {t.category:<12} | {t.amount:>8.2f} | {t.note}")


def run() -> None:
    store = JsonStore()
    ledger: Ledger = store.load()

    while True:
        print(MENU)
        choice = _prompt("Choose (1-12): ")

        if choice == "12":
            store.save(ledger)
            print("Saved. Bye!")
            break

        try:
            if choice == "1":
                tx_date = _prompt("Date (YYYY-MM-DD): ")
                tx_type = _prompt("Type (income/expense): ")
                category = _prompt("Category: ")
                amount = float(_prompt("Amount: "))
                note = _prompt("Note (optional): ")
                ledger.create(tx_date, tx_type, category, amount, note)
                print("Added.\n")

            elif choice == "2":
                txs = ledger.list_all()
                if not txs:
                    print("No transactions yet.\n")
                else:
                    for t in txs:
                        _print_tx(t)
                    print()

        except Exception as e:
            print(f"Error: {e}\n")
