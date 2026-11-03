"""Data-derived engagement metrics, with no writes to historical learning rows."""
from datetime import date, timedelta, datetime, timezone
from sqlalchemy import select
from . import models as m


def active_streak(days, today=None):
    """Consecutive learning days through today (or yesterday before first activity)."""
    today = today or date.today()
    active = {d.day for d in days if (d.minutes or 0) > 0 or (d.xp or 0) > 0}
    end = today if today.isoformat() in active else today - timedelta(days=1)
    count = 0
    while end.isoformat() in active and end <= today:
        count += 1
        end -= timedelta(days=1)
    return count


def get_streak(db, user_id, today=None):
    return active_streak(db.scalars(select(m.DailyActivity).where(m.DailyActivity.user_id == user_id)).all(), today)


def review_due(state, at=None):
    if state is None or state.due_at is None:
        return True
    due = state.due_at
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return due <= (at or datetime.now(timezone.utc))


def schedule_review(state, rating, at=None):
    """Small deterministic interval ladder; not a validated adaptive memory model."""
    at = at or datetime.now(timezone.utc)
    if rating == 'known':
        repeats = (state.repetitions or 0) + 1
        interval = min(90, [1, 3, 7, 14, 30, 60, 90][min(repeats - 1, 6)])
    else:
        repeats, interval = 0, 1
    state.state = rating
    state.repetitions = repeats
    state.interval_days = interval
    state.last_reviewed_at = at
    state.due_at = at + timedelta(days=interval)
    state.updated_at = at
    return state
