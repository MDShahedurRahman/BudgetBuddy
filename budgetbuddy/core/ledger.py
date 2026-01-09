from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Sequence

from .models import Transaction, TxType


def parse_date_iso(d: str) -> date:
    return date.fromisoformat(d)
