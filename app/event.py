from datetime import datetime

from flask_login import current_user

from db import db, Event, EventJoin, User


def new_event(data):
    try:
        name = data["event_name"]
        date = datetime.strptime(data["year"] + data["month"] + data["day"], "%Y%m%d").date()
        time = datetime.strptime(data["hour"] + data["minute"] + data["second"], "%H%M%S").time()
        venue = data["venue"]
        description = data["description"]
    except Exception:
        return False
    user = current_user
    if db.session.execute(db.select(Event).filter_by(name=name)).scalar_one_or_none() is None:
        new_event = Event(name=name, date=date, time=time, venue=venue, description=description, creator=user.id)
        db.session.add(new_event)
        db.session.commit()
        return True
    else:
        return False


def joined_event(event_id, user_id):
    return db.session.execute(db.select(EventJoin).filter_by(event=event_id, participant=user_id)).scalar_one_or_none() is not None


def join_event(event_id, user_id):
    if not joined_event(event_id, user_id):
        new_join = EventJoin(event=event_id, participant=user_id)
        db.session.add(new_join)
        db.session.commit()
        return True
    return False


def get_events(creator=None):
    if creator is None:
        return db.session.execute(db.select(Event)).scalars()
    else:
        return db.session.execute(db.select(Event).filter_by(creator=creator)).scalars()


def get_event(id):
    return db.session.execute(db.select(Event).filter_by(id=id)).scalar_one_or_none()


def get_participants(event):
    return db.session.execute(
        db.select(User).join(EventJoin, EventJoin.participant == User.id).filter_by(event=event.id)).scalars()
