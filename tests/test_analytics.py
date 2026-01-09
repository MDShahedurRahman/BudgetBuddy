import pytest
from budgetbuddy.core.ledger import Ledger
from budgetbuddy.core.analytics import monthly_summary, top_categories, daily_spend_trend


def test_monthly_summary():
    led = Ledger()
    led.create("2026-01-01", "income", "Salary", 2000)
    led.create("2026-01-02", "expense", "Food", 50)
    led.create("2026-01-03", "expense", "Rent", 800)

    s = monthly_summary(led, "2026-01")
    assert s.income == 2000.0
    assert s.expense == 850.0
    assert s.net == 1150.0


def test_top_categories_n():
    led = Ledger()
    led.create("2026-01-01", "expense", "Food", 50)
    led.create("2026-01-02", "expense", "Food", 30)
    led.create("2026-01-03", "expense", "Rent", 800)

    top = top_categories(led, "2026-01", n=1)
    assert top[0][0] == "Rent"
    assert top[0][1] == 800.0

    with pytest.raises(ValueError):
        top_categories(led, "2026-01", n=0)
