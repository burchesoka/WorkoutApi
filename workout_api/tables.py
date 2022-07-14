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
    Table,
    MetaData,
)


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

user = Table(
    'users',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(100)),
    Column('phone', BigInteger, unique=True),
    Column('status', String),
    Column('telegram_id', BigInteger, unique=True, index=True, nullable=True),
)

user_stats = Table(
    'user_stats',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('visited_events', Integer, nullable=True),
    Column('skipped_events', Integer, nullable=True),
    Column('paid_total', Integer, nullable=True),
    Column('user_id', ForeignKey('users.id')),
)

user_profile = Table(
    'user_profiles',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('city', String(25), nullable=True),
    Column('gender', String(10), nullable=True),
    Column('birthday', Date, nullable=True),
    Column('date_created', DateTime, default=datetime.utcnow()),  # server_default=func.now() instead default=...?
    Column('date_updated', DateTime, default=datetime.utcnow()),
    Column('user_id', ForeignKey('users.id')),
)

group = Table(
    'groups',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('title', String(50)),
    Column('trainer_telegram_id', ForeignKey('trainers.telegram_id'), index=True),
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
    Column('trainer_id', ForeignKey('trainers.id')),
)

trainer_stats = Table(
    'trainer_stats',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('visited_events', Integer, nullable=True),
    Column('skipped_events', Integer, nullable=True),
    Column('paid_total', Integer, nullable=True),
    Column('trainer_id', ForeignKey('trainers.id')),
)

payment = Table(
    'payments',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('sum', Integer),
    Column('workouts_left', Integer),
    Column('datetime', DateTime, default=datetime.utcnow()),
    Column('user_id', ForeignKey('users.id'), index=True),
    Column('group_id', ForeignKey('groups.id'), index=True),
)
