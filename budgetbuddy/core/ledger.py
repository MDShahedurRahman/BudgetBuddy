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
