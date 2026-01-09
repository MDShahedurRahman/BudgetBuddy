from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from budgetbuddy.core.ledger import Ledger


class JsonStore:
    def __init__(self, db_file: Path | None = None) -> None:
        self.db_file = db_file or get_paths().db_file

    def load(self) -> Ledger:
        if not self.db_file.exists():
            return Ledger()

        try:
            data = json.loads(self.db_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return Ledger()

        return Ledger.from_dict(data)

    def save(self, ledger: Ledger) -> None:
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self.db_file.write_text(json.dumps(
            ledger.to_dict(), indent=2), encoding="utf-8")
