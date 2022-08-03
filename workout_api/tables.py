from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Date,
    ForeignKey,
    Integer,
    BigInteger,
    Numeric,
    String,
    Boolean,
    Table,
    MetaData,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(BigInteger, unique=True)
    status = Column(String)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=True)


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(BigInteger, primary_key=True)
    city = Column(String(25), nullable=True)
    gender = Column(String(10), nullable=True)
    birthday = Column(Date, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow())  # server_default=func.now() instead default=...?
    date_updated = Column(DateTime, default=datetime.utcnow())
    user_id = Column(ForeignKey('users.id'), index=True)

    # user = relationship('User', backref=backref('profile', lazy='joined'))


class UserStats(Base):
    __tablename__ = 'user_stats'

    id = Column(BigInteger, primary_key=True)
    visited_events = Column(Integer, nullable=True)
    skipped_events = Column(Integer, nullable=True)
    paid_total = Column(Integer, nullable=True)
    user_id = Column(ForeignKey('users.id'), index=True)

    # user = relationship('User', backref=backref('stats', lazy='joined'))


group = Table(
    'groups',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('title', String(50)),
    Column('trainer_telegram_id', ForeignKey('trainers.telegram_id'), index=True),
    Column('timetable', String),
    # Column('city', String),
    # Column('address', String),
)

users_groups = Table(
    "users_groups",
    metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_name_for_trainer", String(50)),
)

trainer = Table(
    'trainers',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(100)),
    Column('phone', BigInteger, unique=True),
    Column('telegram_id', BigInteger, unique=True, index=True, nullable=True),
)

trainer_profile = Table(
    'trainer_profiles',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('city', String(25), nullable=True),
    Column('specialization', String(25), nullable=True),  # TODO отдельную таблицу, если у тренеров несколько специализаций?
    Column('gender', String(10), nullable=True),
    Column('birthday', Date, nullable=True),
    Column('date_created', DateTime, default=datetime.utcnow()),  # server_default=func.now() instead default=...?
    Column('date_updated', DateTime, default=datetime.utcnow()),
    Column('trainer_id', ForeignKey('trainers.id'), index=True),
)

trainer_stats = Table(
    'trainer_stats',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('visited_events', Integer, nullable=True),
    Column('skipped_events', Integer, nullable=True),
    Column('paid_total', Integer, nullable=True),
    Column('trainer_id', ForeignKey('trainers.id'), index=True),
)

payment = Table(
    'payments',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('sum', Integer),
    Column('workouts_left', Integer),
    Column('datetime', DateTime, default=datetime.utcnow()),
    Column('user_telegram_id', ForeignKey('users.telegram_id'), index=True),
    Column('group_id', ForeignKey('groups.id'), index=True),
    Column('verified', Boolean, default=False),
    Column('comment', String, nullable=True),
)

event = Table(
    'events',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('user_telegram_id', ForeignKey('users.telegram_id'), index=True),
    Column('group_id', ForeignKey('groups.id'), index=True),
    Column('datetime', DateTime),
)
