import pytest
from budgetbuddy.core.ledger import Ledger


def test_create_and_list_sorted():
    led = Ledger()
    led.create("2026-01-02", "expense", "Food", 10, "Lunch")
    led.create("2026-01-01", "income", "Salary", 1000, "Paycheck")
    txs = led.list_all()
    assert len(txs) == 2
    assert txs[0].tx_date == "2026-01-01"
