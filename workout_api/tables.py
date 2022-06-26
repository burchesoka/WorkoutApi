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
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    phone = Column(Integer, unique=True)


class User(BaseUser):
    __tablename__ = 'users'

    status = Column(String)


class Trainer(BaseUser):
    __tablename__ = 'trainers'


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), index=True)

    users = relationship("User", secondary=users_groups_table)
    trainer = relationship("Trainer", backref='groups')
