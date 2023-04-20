from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(Integer, unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Event(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    venue = Column(String, nullable=False)
    description = Column(String)
    creator = Column("user_id", ForeignKey(User.id), nullable=False)


class EventJoin(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column("event", ForeignKey(Event.id), nullable=False)
    participant = Column("user", ForeignKey(User.id), nullable=False)
