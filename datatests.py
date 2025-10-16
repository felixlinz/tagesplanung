import os
import csv
import pytest
from tempfile import TemporaryDirectory
from data_manager import EmployeeTaskLogManager  # ← change to your actual filename

# ---------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------

@pytest.fixture
def mgr(tmp_path):
    """Provides a fresh manager instance in an isolated temp directory."""
    path = tmp_path / "employee_log.csv"
    return EmployeeTaskLogManager(filename=str(path))

# ---------------------------------------------------------------------
# BASIC INTERNALS
# ---------------------------------------------------------------------

def test_sort_key_numeric_vs_text():
    assert EmployeeTaskLogManager._sort_key("10") == (0, 10)
    assert EmployeeTaskLogManager._sort_key("A") == (1, "a")
    # sorting: numeric before alpha, ascending
    vals = ["B", "2", "10", "a", "1"]
    sorted_vals = sorted(vals, key=EmployeeTaskLogManager._sort_key)
    assert sorted_vals == ["1", "2", "10", "a", "B"]

# ---------------------------------------------------------------------
# RESET + EMPTY LOAD
# ---------------------------------------------------------------------

def test_reset_and_empty_load(mgr):
    # start clean
    mgr.reset_log()
    assert os.path.exists(mgr.filename)
    assert mgr._load_log() == []  # file only has header

# ---------------------------------------------------------------------
# INCREMENT LOGIC
# ---------------------------------------------------------------------

def test_increment_creates_new_file_and_employee_and_task(mgr):
    # Initially no file
    mgr.reset_log()
    mgr.increment_task_count({"Becker": "1"})
    data = mgr.get_all()
    assert data[0]["Name"] == "Becker"
    assert data[0]["1"] == "1"  # first increment = 1
    # add another task
    mgr.increment_task_count({"Becker": "FD"})
    summary = mgr.get_employee_summary("Becker")
    assert summary["FD"] == 1
    assert summary["1"] == 1

def test_increment_adds_new_employee_and_existing_tasks(mgr):
    mgr.reset_log()
    mgr.increment_task_count({"Becker": "1"})
    mgr.increment_task_count({"Zimmermann": "1"})
    # Both should now exist
    all_data = mgr.get_all()
    names = [r["Name"] for r in all_data]
    assert {"Becker", "Zimmermann"} <= set(names)
    # Both have "1" task column
    for row in all_data:
        assert "1" in row

def test_increment_invalid_inputs(mgr):
    with pytest.raises(ValueError):
        mgr.increment_task_count({})
    with pytest.raises(ValueError):
        mgr.increment_task_count({"A": "1", "B": "2"})

def test_increment_case_insensitive_name_and_task(mgr):
    mgr.reset_log()
    mgr.increment_task_count({"becker": "x"})
    mgr.increment_task_count({"Becker": "X"})  # same employee & task, different case
    summary = mgr.get_employee_summary("BECKER")

    # keys may differ in case; normalize
    key_lower_map = {k.lower(): v for k, v in summary.items()}
    assert key_lower_map["x"] == 2  # both increments merged

def test_increment_new_task_added_to_all_existing_employees(mgr):
    mgr.reset_log()
    mgr.increment_task_count({"Becker": "1"})
    mgr.increment_task_count({"Zimmermann": "2"})
    # Add a new task "FD" — should appear for both
    mgr.increment_task_count({"Becker": "FD"})
    all_data = mgr.get_all()
    for row in all_data:
        assert "FD" in row

# ---------------------------------------------------------------------
# SUMMARY + GET ALL
# ---------------------------------------------------------------------

def test_get_employee_summary_and_all(mgr):
    mgr.reset_log()
    mgr.increment_task_count({"Becker": "1"})
    mgr.increment_task_count({"Becker": "1"})
    summary = mgr.get_employee_summary("Becker")
    assert summary["1"] == 2
    # Nonexistent employee
    assert mgr.get_employee_summary("Unknown") == {}
    # get_all returns list
    assert isinstance(mgr.get_all(), list)

# ---------------------------------------------------------------------
# TOP EMPLOYEES
# ---------------------------------------------------------------------

def test_get_top_employees_for_task_sorted_and_filtered(mgr):
    mgr.reset_log()
    # populate
    for _ in range(5):
        mgr.increment_task_count({"Becker": "10"})
    for _ in range(3):
        mgr.increment_task_count({"Zimmermann": "10"})
    for _ in range(1):
        mgr.increment_task_count({"Lange": "10"})
    # plus one unrelated task to ensure filtering
    mgr.increment_task_count({"Becker": "X"})

    top = mgr.get_top_employees_for_task("10", top_n=3)
    assert top == [("Becker", 5), ("Zimmermann", 3), ("Lange", 1)]

    # filter excludes those with 0 count
    zero_task_top = mgr.get_top_employees_for_task("999")
    assert zero_task_top == []

def test_get_top_employees_case_insensitive_and_limit(mgr):
    mgr.reset_log()
    mgr.increment_task_count({"A": "x"})
    mgr.increment_task_count({"B": "X"})
    mgr.increment_task_count({"B": "x"})
    mgr.increment_task_count({"C": "x"})
    top2 = mgr.get_top_employees_for_task("X", top_n=2)
    # B has 2, others have 1 → only two returned
    assert top2 == [("B", 2), ("A", 1)]

def test_get_top_employees_with_non_integer_values(mgr):
    mgr.reset_log()
    # manually write malformed numeric values
    data = [
        {"Name": "Becker", "X": "notnum"},
        {"Name": "Zimmermann", "X": "2"},
    ]
    mgr._save_log(data)
    top = mgr.get_top_employees_for_task("x")
    # should treat 'notnum' as 0 and ignore Becker
    assert top == [("Zimmermann", 2)]

def test_get_top_employees_with_empty_log(mgr):
    mgr.reset_log()
    # ensure empty returns []
    assert mgr.get_top_employees_for_task("X") == []

# ---------------------------------------------------------------------
# FILE PERSISTENCE INTEGRITY
# ---------------------------------------------------------------------

def test_save_and_reload_persistence(mgr):
    mgr.reset_log()
    mgr.increment_task_count({"Becker": "1"})
    mgr.increment_task_count({"Becker": "FD"})
    mgr.increment_task_count({"Zimmermann": "FD"})

    # reload a new manager using same file
    new_mgr = EmployeeTaskLogManager(filename=mgr.filename)
    loaded = new_mgr._load_log()
    assert any(row["Name"] == "Becker" for row in loaded)
    assert any("FD" in row for row in loaded)
