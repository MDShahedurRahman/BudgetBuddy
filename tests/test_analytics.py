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
