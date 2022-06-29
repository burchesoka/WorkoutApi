from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


users_groups_table = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class BaseUser(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(Integer, unique=True)


class User(BaseUser):
    __tablename__ = 'users'

    status = Column(String)
    telegram_id = Column(Integer, unique=True, index=True, nullable=True)

    profile = relationship('Profile', backref='users', uselist=False)
    stats = relationship('UserStats', backref='users', uselist=False)
    # groups = relationship('Group', secondary=users_groups_table) -- конфликтуе


class Trainer(BaseUser):
    __tablename__ = 'trainers'

    telegram_id = Column(Integer, unique=True, index=True, nullable=True)


class NotRegisteredUser(BaseUser):
    __tablename__ = 'not_registered_users'

    # TODO когда сделаю группы и тренеров
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    group = relationship('Group', backref='not_registered_users')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), index=True)

    users = relationship("User", secondary=users_groups_table)
    trainer = relationship("Trainer", backref='groups')


class UserStats(Base):
    __tablename__ = 'user_stats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    visited_events = Column(Integer, nullable=True)
    skipped_events = Column(Integer, nullable=True)


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    city = Column(String(25), nullable=True)
    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow())
    date_updated = Column(DateTime, default=datetime.utcnow())
