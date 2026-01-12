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

            elif choice == "3":
                month = _prompt("Month (YYYY-MM) [blank=all]: ")
                category = _prompt("Category [blank=all]: ")
                tx_type = _prompt("Type income/expense [blank=all]: ")
                txs = ledger.filter(
                    month=month or None, category=category or None, tx_type=tx_type or None)
                if not txs:
                    print("No matches.\n")
                else:
                    for t in txs:
                        _print_tx(t)
                    print()

            elif choice == "4":
                tx_id = _prompt("Transaction id: ")
                tx_date = _prompt("New date (YYYY-MM-DD) [blank=keep]: ")
                tx_type = _prompt("New type income/expense [blank=keep]: ")
                category = _prompt("New category [blank=keep]: ")
                amount_txt = _prompt("New amount [blank=keep]: ")
                note = _prompt("New note [blank=keep]: ")

                updated = ledger.update(
                    tx_id,
                    tx_date=tx_date or None,
                    tx_type=tx_type or None,
                    category=category or None,
                    amount=float(amount_txt) if amount_txt else None,
                    note=note or None,
                )
                print("Updated:")
                _print_tx(updated)
                print()

            elif choice == "5":
                tx_id = _prompt("Transaction id: ")
                ok = ledger.delete(tx_id)
                print("Deleted.\n" if ok else "Not found.\n")

            elif choice == "6":
                month = _prompt("Month (YYYY-MM): ")
                s = monthly_summary(ledger, month)
                print(f"\nMonth: {s.month}")
                print(f"Income : {s.income:.2f}")
                print(f"Expense: {s.expense:.2f}")
                print(f"Net    : {s.net:.2f}\n")

            elif choice == "7":
                month = _prompt("Month (YYYY-MM): ")
                n_txt = _prompt("Top N (default 5): ")
                n = int(n_txt) if n_txt else 5
                top = top_categories(ledger, month, n=n, tx_type="expense")
                if not top:
                    print("No expenses found.\n")
                else:
                    print()
                    for cat, amt in top:
                        print(f"{cat}: {amt:.2f}")
                    print()

        except Exception as e:
            print(f"Error: {e}\n")
