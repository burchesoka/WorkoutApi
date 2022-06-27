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
    name = Column(String)
    phone = Column(Integer, unique=True)


class User(BaseUser):
    __tablename__ = 'users'

    status = Column(String)
    telegram_id = Column(Integer, unique=True, index=True, nullable=True)
    stats_id = Column(Integer, ForeignKey('user_stats.id'))

    stats = relationship('UserStats', backref='stats')


class Trainer(BaseUser):
    __tablename__ = 'trainers'

    telegram_id = Column(Integer, unique=True, index=True, nullable=True)


class NotRegisteredUser(BaseUser):
    __tablename__ = 'not_registered_users'

    # TODO когда сделаю группы и тренеров
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    group = relationship('Group', backref='group')


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
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    visited_events = Column(Integer)
    skipped_events = Column(Integer)
