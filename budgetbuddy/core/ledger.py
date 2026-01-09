from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Sequence

from .models import Transaction, TxType


def parse_date_iso(d: str) -> date:
    return date.fromisoformat(d)


def ensure_positive_amount(amount: float) -> None:
    if amount is None or float(amount) <= 0:
        raise ValueError("Amount must be a positive number.")


def normalize_category(cat: str) -> str:
    cat = (cat or "").strip()
    if not cat:
        raise ValueError("Category cannot be empty.")
    return cat


def normalize_note(note: str) -> str:
    return (note or "").strip()


def normalize_type(t: str) -> TxType:
    t = (t or "").strip().lower()
    if t not in ("income", "expense"):
        raise ValueError("Type must be 'income' or 'expense'.")
    return t  # type: ignore[return-value]


def month_key(iso_date: str) -> str:
    # "YYYY-MM-DD" -> "YYYY-MM"
    return iso_date[:7]


class Ledger:
    """
    Stores transactions and provides CRUD + filtering.
    """

    def __init__(self) -> None:
        self._tx: Dict[str, Transaction] = {}

    def add(self, tx: Transaction) -> Transaction:
        # Validate
        parse_date_iso(tx.tx_date)
        normalize_type(tx.tx_type)
        normalize_category(tx.category)
        ensure_positive_amount(tx.amount)

        if tx.id in self._tx:
            raise ValueError("Transaction id already exists.")
        self._tx[tx.id] = tx
        return tx

    def create(self, tx_date: str, tx_type: str, category: str, amount: float, note: str = "") -> Transaction:
        tx_date = tx_date.strip()
        parse_date_iso(tx_date)
        ttype = normalize_type(tx_type)
        cat = normalize_category(category)
        ensure_positive_amount(amount)
        note = normalize_note(note)

        tx = Transaction.new(tx_date=tx_date, tx_type=ttype,
                             category=cat, amount=float(amount), note=note)
        return self.add(tx)

    def list_all(self) -> List[Transaction]:
        return sorted(self._tx.values(), key=lambda t: (t.tx_date, t.tx_type, t.category, t.amount, t.id))

    def get(self, tx_id: str) -> Optional[Transaction]:
        return self._tx.get(tx_id)

    def delete(self, tx_id: str) -> bool:
        return self._tx.pop(tx_id, None) is not None

    def update(
        self,
        tx_id: str,
        tx_date: Optional[str] = None,
        tx_type: Optional[str] = None,
        category: Optional[str] = None,
        amount: Optional[float] = None,
        note: Optional[str] = None,
    ) -> Transaction:
        current = self._tx.get(tx_id)
        if current is None:
            raise KeyError("Transaction not found.")

        new_date = current.tx_date if tx_date is None else tx_date.strip()
        parse_date_iso(new_date)

        new_type = current.tx_type if tx_type is None else normalize_type(
            tx_type)
        new_cat = current.category if category is None else normalize_category(
            category)

        new_amount = current.amount if amount is None else float(amount)
        ensure_positive_amount(new_amount)

        new_note = current.note if note is None else normalize_note(note)

        updated = Transaction(
            id=current.id,
            tx_date=new_date,
            tx_type=new_type,
            category=new_cat,
            amount=new_amount,
            note=new_note,
        )
        self._tx[tx_id] = updated
        return updated

    def filter(
        self,
        month: Optional[str] = None,        # "YYYY-MM"
        category: Optional[str] = None,
        tx_type: Optional[str] = None,      # income/expense
    ) -> List[Transaction]:
        month = (month or "").strip()
        category = (category or "").strip()
        tx_type = (tx_type or "").strip()

        if month and (len(month) != 7 or month[4] != "-"):
            raise ValueError("Month must be in YYYY-MM format.")

        if tx_type:
            tx_type = normalize_type(tx_type)

        out: List[Transaction] = []
        for t in self._tx.values():
            if month and month_key(t.tx_date) != month:
                continue
            if category and t.category.lower() != category.lower():
                continue
            if tx_type and t.tx_type != tx_type:
                continue
            out.append(t)

        return sorted(out, key=lambda t: (t.tx_date, t.tx_type, t.category, t.amount, t.id))

    # ---- persistence helpers ----
    def to_dict(self) -> Dict:
        return {
            "transactions": [
                {
                    "id": t.id,
                    "tx_date": t.tx_date,
                    "tx_type": t.tx_type,
                    "category": t.category,
                    "amount": t.amount,
                    "note": t.note,
                }
                for t in self.list_all()
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Ledger":
        led = cls()
        for item in data.get("transactions", []):
            tx = Transaction(
                id=item["id"],
                tx_date=item["tx_date"],
                tx_type=item["tx_type"],
                category=item["category"],
                amount=float(item["amount"]),
                note=item.get("note", "") or "",
            )
            led.add(tx)
        return led
