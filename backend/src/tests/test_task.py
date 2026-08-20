from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

import backend.src.model.entities.task as task_module
from backend.src.model.entities.task import Task


def _future_date(days: int = 30) -> datetime:
    return datetime.now() + timedelta(days=days)


def test_properties_expose_constructor_values():
    limit_date = _future_date()

    task = Task("Write report", limit_date)

    assert task.description == "Write report"
    assert task.limit_date == limit_date
    assert task.is_completed is False


def test_mark_completed_sets_is_completed_true():
    task = Task("Write report", _future_date())

    task.mark_completed()

    assert task.is_completed is True


def test_is_overdue_true_when_limit_date_passed_and_not_completed():
    limit_date = _future_date(days=1)
    task = Task("Write report", limit_date)

    with patch.object(task_module, "datetime") as mock_datetime:
        mock_datetime.now.return_value = limit_date + timedelta(days=1)
        assert task.is_overdue() is True


def test_is_overdue_false_when_limit_date_in_future():
    task = Task("Write report", _future_date(days=1))

    assert task.is_overdue() is False


def test_is_overdue_false_when_completed_even_if_limit_date_passed():
    limit_date = _future_date(days=1)
    task = Task("Write report", limit_date)
    task.mark_completed()

    with patch.object(task_module, "datetime") as mock_datetime:
        mock_datetime.now.return_value = limit_date + timedelta(days=1)
        assert task.is_overdue() is False


def test_repr_shows_description_limit_date_and_is_completed():
    limit_date = _future_date()
    task = Task("Write report", limit_date)

    assert repr(task) == (
        "Task(description='Write report', "
        f"limit_date={limit_date!r}, is_completed=False)"
    )


def test_equal_when_description_limit_date_and_is_completed_match():
    limit_date = _future_date()

    task_a = Task("Write report", limit_date)
    task_b = Task("Write report", limit_date)

    assert task_a == task_b


def test_not_equal_when_description_differs():
    limit_date = _future_date()

    task_a = Task("Write report", limit_date)
    task_b = Task("Send invoice", limit_date)

    assert task_a != task_b


def test_init_raises_value_error_when_limit_date_is_in_the_past():
    past_date = datetime.now() - timedelta(days=1)

    with pytest.raises(ValueError):
        Task("Write report", past_date)
