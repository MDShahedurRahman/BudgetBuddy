from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal
from uuid import uuid4


TxType = Literal["income", "expense"]


@dataclass(frozen=True)
class Transaction:
    id: str
    tx_date: str          # YYYY-MM-DD
    tx_type: TxType       # "income" | "expense"
    category: str
    amount: float         # positive number
    note: str = ""

    @staticmethod
    def new(tx_date: str, tx_type: TxType, category: str, amount: float, note: str = "") -> "Transaction":
        return Transaction(
            id=str(uuid4()),
            tx_date=tx_date,
            tx_type=tx_type,
            category=category,
            amount=float(amount),
            note=note or "",
        )


def today_iso() -> str:
    return date.today().isoformat()
