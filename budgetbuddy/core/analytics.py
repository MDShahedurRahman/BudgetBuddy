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
