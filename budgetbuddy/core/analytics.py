from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .ledger import Ledger, month_key


@dataclass(frozen=True)
class MonthlySummary:
    month: str
    income: float
    expense: float
    net: float


def monthly_summary(ledger: Ledger, month: str) -> MonthlySummary:
    txs = ledger.filter(month=month)
    income = sum(t.amount for t in txs if t.tx_type == "income")
    expense = sum(t.amount for t in txs if t.tx_type == "expense")
    net = income - expense
    return MonthlySummary(month=month, income=income, expense=expense, net=net)


def category_totals(ledger: Ledger, month: str, tx_type: str = "expense") -> Dict[str, float]:
    txs = ledger.filter(month=month, tx_type=tx_type)
    totals: Dict[str, float] = {}
    for t in txs:
        key = t.category
        totals[key] = totals.get(key, 0.0) + float(t.amount)
    return dict(sorted(totals.items(), key=lambda kv: (-kv[1], kv[0].lower())))
