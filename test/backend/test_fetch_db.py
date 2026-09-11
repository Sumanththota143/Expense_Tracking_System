from backend.fetch_db import fetch_by_date
from datetime import date

def test_one_record():
    record  = fetch_by_date('2026-08-20')
    assert record[0]['expense_date'] == date(2026, 8, 20)
    assert record[1]['notes'] == 'Lunch'
    assert record[6]['category'] == 'Bills'

# def test_total_records_by_date():
#     record = fetch_by_date("2026-08-30")
#     assert len(record) == 1