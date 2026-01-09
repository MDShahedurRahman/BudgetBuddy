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


def top_categories(ledger: Ledger, month: str, n: int = 5, tx_type: str = "expense") -> List[Tuple[str, float]]:
    if n <= 0:
        raise ValueError("n must be > 0")
    totals = category_totals(ledger, month=month, tx_type=tx_type)
    items = list(totals.items())
    return items[:n]


def daily_spend_trend(ledger: Ledger, month: str) -> List[Tuple[str, float]]:
    """
    Returns list of (YYYY-MM-DD, total_expense_that_day) for the given month.
    Only includes days that have at least one expense.
    """
    txs = ledger.filter(month=month, tx_type="expense")
    totals: Dict[str, float] = {}
    for t in txs:
        totals[t.tx_date] = totals.get(t.tx_date, 0.0) + float(t.amount)
    return sorted(totals.items(), key=lambda kv: kv[0])
