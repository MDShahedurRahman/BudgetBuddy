import pytest
from budgetbuddy.core.ledger import Ledger


def test_create_and_list_sorted():
    led = Ledger()
    led.create("2026-01-02", "expense", "Food", 10, "Lunch")
    led.create("2026-01-01", "income", "Salary", 1000, "Paycheck")
    txs = led.list_all()
    assert len(txs) == 2
    assert txs[0].tx_date == "2026-01-01"


def test_filter_by_month_and_type():
    led = Ledger()
    led.create("2026-01-02", "expense", "Food", 10)
    led.create("2026-02-01", "expense", "Food", 20)
    jan = led.filter(month="2026-01")
    assert len(jan) == 1
    assert jan[0].amount == 10.0

    feb_exp = led.filter(month="2026-02", tx_type="expense")
    assert len(feb_exp) == 1


def test_update_and_delete():
    led = Ledger()
    tx = led.create("2026-01-02", "expense", "Food", 10)
    updated = led.update(tx.id, amount=12.5, note="Dinner")
    assert updated.amount == 12.5
    assert updated.note == "Dinner"

    assert led.delete(tx.id) is True
    assert led.get(tx.id) is None


def test_validation_amount_positive():
    led = Ledger()
    with pytest.raises(ValueError):
        led.create("2026-01-01", "expense", "Food", 0)
