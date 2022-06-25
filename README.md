Чтобы создать таблицы в бд, в консоли пишем:

from workout_api.database import engine
from workout_api.tables import Base
Base.metadata.create_all(engine)
