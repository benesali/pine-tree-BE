from datetime import date
from unittest.mock import Mock

import pytest

from app.models.availability import AvailabilityStatus
from app.services.calendar import CalendarService


@pytest.mark.unit
def test_date_range_inclusive():
    svc = CalendarService(Mock())
    days = list(svc._date_range(date(2025, 7, 10), date(2025, 7, 12)))
    assert days == [date(2025, 7, 10), date(2025, 7, 11), date(2025, 7, 12)]


@pytest.mark.unit
def test_set_range_inserts_and_updates(monkeypatch):
    mock_db = Mock()
    # simulate no existing for all days
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    svc = CalendarService(mock_db)
    svc.set_range(
        1, date(2025, 7, 10), date(2025, 7, 11), AvailabilityStatus.blocked, "note"
    )

    # expect two adds and one commit
    assert mock_db.add.call_count == 2
    mock_db.commit.assert_called_once()


@pytest.mark.unit
def test_set_range_raises_on_booked_conflict():
    mock_db = Mock()
    existing = Mock()
    existing.status = AvailabilityStatus.booked
    # first day has existing booked, so should raise ValueError
    mock_db.query.return_value.filter_by.return_value.first.side_effect = [
        existing,
        None,
    ]

    svc = CalendarService(mock_db)
    with pytest.raises(ValueError):
        svc.set_range(
            1, date(2025, 7, 10), date(2025, 7, 11), AvailabilityStatus.blocked
        )


@pytest.mark.unit
def test_clear_range_calls_delete_and_commit():
    mock_db = Mock()
    svc = CalendarService(mock_db)
    svc.clear_range(1, date(2025, 7, 10), date(2025, 7, 12))

    # assert delete was called on the query chain and commit called
    mock_db.query.return_value.filter.return_value.delete.assert_called_once_with(
        synchronize_session=False
    )
    mock_db.commit.assert_called_once()
