from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

from .settings import settings


database = Database(
    f'postgresql://{settings.db_user}:{settings.db_pass}@'
    f'{settings.db_host}:5432/{settings.db_name}',
)


async def get_session():

    try:
        print('YIELD')
        yield await database.connect()
        print('AFTER YIELD')
    finally:
        await database.disconnect()
        print('CLOSED SESSION')



''' OLD '''
engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False},
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
