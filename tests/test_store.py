from pathlib import Path
from budgetbuddy.storage.json_store import JsonStore
from budgetbuddy.storage.csv_io import export_csv, import_csv
from budgetbuddy.core.ledger import Ledger


def test_json_store_save_load(tmp_path):
    db = tmp_path / "db.json"
    store = JsonStore(db_file=db)

    led = Ledger()
    led.create("2026-01-01", "income", "Salary", 1000)
    store.save(led)

    loaded = store.load()
    assert len(loaded.list_all()) == 1
    assert loaded.list_all()[0].category == "Salary"
