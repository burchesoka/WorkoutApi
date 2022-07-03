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
    # relationship???
)

user_stats = Table(
    'user_stats',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('visited_events', Integer, nullable=True),
    Column('skipped_events', Integer, nullable=True),
)

profile = Table(
    'profiles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('city', String(25), nullable=True),
    Column('gender', String(10), nullable=True),
    Column('birthday', Date, nullable=True),
    Column('date_created', DateTime, default=datetime.utcnow()),  # server_default=func.now() instead default=...?
    Column('date_updated', DateTime, default=datetime.utcnow()),
)

group = Table(
    'groups',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('group_name', String),
    Column('trainer_id', Integer, ForeignKey('trainers.id'), index=True),
)

users_groups_table = Table(
    "users_groups",
    metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

trainer = Table(
    'trainers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('phone', Integer, unique=True),
    Column('telegram_id', Integer, unique=True, index=True, nullable=True),
)
