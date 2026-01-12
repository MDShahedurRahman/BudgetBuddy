from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

from budgetbuddy.core.ledger import Ledger
from budgetbuddy.core.models import Transaction


CSV_HEADERS = ["id", "tx_date", "tx_type", "category", "amount", "note"]


def export_csv(ledger: Ledger, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        w.writeheader()
        for t in ledger.list_all():
            w.writerow(
                {
                    "id": t.id,
                    "tx_date": t.tx_date,
                    "tx_type": t.tx_type,
                    "category": t.category,
                    "amount": f"{t.amount:.2f}",
                    "note": t.note,
                }
            )


def import_csv(path: Path) -> Ledger:
    led = Ledger()
    with path.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            tx = Transaction(
                id=row["id"],
                tx_date=row["tx_date"],
                tx_type=row["tx_type"],  # validated by Ledger.add
                category=row["category"],
                amount=float(row["amount"]),
                note=row.get("note", "") or "",
            )
            led.add(tx)
    return led
