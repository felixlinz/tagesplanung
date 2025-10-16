import pytest
from unittest.mock import Mock
from logicmanager import TourAssigner  # ← replace with your actual module filename

# ---------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------

@pytest.fixture
def sample_data():
    """Representative grouped employee data for tests."""
    return {
        "Stammfahrer": [
            {"Name": "Becker", "Stammtour": 1},
            {"Name": "Zimmermann", "Stammtour": 2},
            {"Name": "Lange", "Stammtour": 3},
        ],
        "Springer": [
            {"Name": "Klein"},
            {"Name": "Schmidt"},
        ],
        "Abrufer": [
            {"Name": "Meyer"},
        ],
        "Frühdienst": [{"Name": "Alpha"}],
        "Spätdienst": [{"Name": "Beta"}],
        "Innendienst": [{"Name": "Gamma"}],
        "Firmen": [{"Name": "Delta"}],
        "Einweisung": [{"Name": "Epsilon"}],
        "Dienstfrei": [{"Name": "Zeta"}],
    }


# ---------------------------------------------------------------------
# BASIC BEHAVIOR
# ---------------------------------------------------------------------

def test_assign_tours_prefers_stammfahrer(sample_data):
    ta = TourAssigner(sample_data)
    result = ta.assign_tours([1, 2])

    assignments = result["assignments"]

    # Stammfahrer Becker → Tour 1, Zimmermann → Tour 2
    assert {"Becker", "Zimmermann"} == {a["driver"] for a in assignments}
    assert all(a["driver"] for a in assignments)

    # Check unassigned includes remaining (Lange, plus all backups)
    assert "Lange" in result["unassigned"]
    assert "Klein" in result["unassigned"]
    assert "Meyer" in result["unassigned"]

    # Other categories passed through
    assert result["Frühdienst"] == ["Alpha"]
    assert result["Dienstfrei"] == ["Zeta"]


def test_assign_tours_with_missing_stammfahrer_uses_backup(sample_data):
    ta = TourAssigner(sample_data)
    # Tour 9 has no Stammfahrer
    result = ta.assign_tours([9])
    assigned = result["assignments"][0]["driver"]

    # Free Stammfahrer + springer + abrufer can all be backups
    assert assigned in {"Becker", "Zimmermann", "Lange", "Klein", "Schmidt", "Meyer"}
    assert assigned  # must not be None
    assert result["unassigned"]  # unassigned backups still exist





def test_assign_tours_with_no_available_backups(sample_data):
    # Remove all categories to simulate empty data
    minimal = {"Stammfahrer": [], "Springer": [], "Abrufer": []}
    ta = TourAssigner(minimal)
    result = ta.assign_tours([5])
    assert result["assignments"][0]["driver"] is None
    assert result["unassigned"] == []


def test_assign_tours_handles_string_and_int_consistency(sample_data):
    # Stammtour numbers as int, requested as string
    ta = TourAssigner(sample_data)
    res = ta.assign_tours(["1"])
    assert res["assignments"][0]["driver"] == "Becker"


# ---------------------------------------------------------------------
# EXPERIENCE-BASED SELECTION
# ---------------------------------------------------------------------

def test_select_best_backup_with_task_log_manager(sample_data):
    """When task_log_manager has experience data, it should be honored."""
    mock_log = Mock()
    # Only "Meyer" has top experience for tour "9"
    mock_log.get_top_employees_for_task.return_value = [("Meyer", 12), ("Klein", 5)]
    ta = TourAssigner(sample_data, task_log_manager=mock_log)

    res = ta.assign_tours([9])
    assigned = res["assignments"][0]["driver"]

    # Should pick the most experienced backup ("Meyer")
    assert assigned == "Meyer"

    # Verify get_top_employees_for_task called properly
    mock_log.get_top_employees_for_task.assert_called_with("9")


def test_select_best_backup_falls_back_if_no_match_in_toplist(sample_data):
    """If top list contains names not in backup pool, fall back to first available."""
    mock_log = Mock()
    mock_log.get_top_employees_for_task.return_value = [("Nonexistent", 10)]
    ta = TourAssigner(sample_data, task_log_manager=mock_log)

    res = ta.assign_tours([99])
    assigned = res["assignments"][0]["driver"]

    # No one in top list matches → fallback to first available backup (which includes free Stammfahrer)
    assert assigned in {"Becker", "Zimmermann", "Lange", "Klein", "Schmidt", "Meyer"}



def test_select_best_backup_without_task_log_manager(sample_data):
    """If no task log manager is provided, picks first available backup."""
    ta = TourAssigner(sample_data)
    result = ta._select_best_backup(sample_data["Springer"], set(), "99")
    assert result == "Klein"  # first available name


def test_select_best_backup_no_available(sample_data):
    ta = TourAssigner(sample_data)
    chosen = ta._select_best_backup([], set(), "1")
    assert chosen is None


# ---------------------------------------------------------------------
# ASSIGNMENT COMPLETENESS + STATE
# ---------------------------------------------------------------------

def test_assignments_and_unassigned_state_persist(sample_data):
    ta = TourAssigner(sample_data)
    res = ta.assign_tours([1, 9])
    # internal state updated
    assert hasattr(ta, "assignments")
    assert isinstance(res["assignments"], list)
    assert ta.unassigned  # unassigned list populated
    assert set(ta.unassigned).issubset(
        {p["Name"] for cat in sample_data.values() for p in cat}
    )


def test_assign_tours_multiple_tours_and_no_duplicates(sample_data):
    """Ensure no driver is assigned to multiple tours."""
    ta = TourAssigner(sample_data)
    res = ta.assign_tours([1, 2, 3, 9])
    assigned_drivers = [a["driver"] for a in res["assignments"] if a["driver"]]
    assert len(assigned_drivers) == len(set(assigned_drivers))
    # Check that unassigned includes at least one name not assigned
    assert any(u not in assigned_drivers for u in res["unassigned"])
